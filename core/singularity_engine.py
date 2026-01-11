import os
import numpy as np
import logging
from typing import List
import gguf

# Configure Logging
logger = logging.getLogger("SingularityCore")
logging.basicConfig(level=logging.INFO)

class SingularityEngine:
    def __init__(self, model_path, output_dir="adapters"):
        self.model_path = model_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        logger.info(f"Initializing Singularity Core with model: {model_path}")
        
        # Load llama-cpp model for embedding extraction
        from llama_cpp import Llama
        try:
            self.llm = Llama(
                model_path=model_path,
                n_ctx=2048,
                embedding=True, # Critical for vector extraction
                verbose=False,
                n_gpu_layers=0  # Force CPU
            )
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise e

    def calculate_concept_vector(self, text_data: str) -> np.ndarray:
        """
        Derives the 'Spectral Lattice' (Concept Vector) from the input data.
        """
        logger.info("Computing Spectral Lattice...")
        
        if not text_data.strip():
            return None

        # Tokenize
        tokens = self.llm.tokenize(text_data.encode("utf-8"))
        
        # Chunking strategy to fit context
        max_chunk = 512
        chunks = [tokens[i:i + max_chunk] for i in range(0, len(tokens), max_chunk)]
        # Limit chunks for speed in "Instant" mode
        chunks = chunks[:10] 
        
        embeddings =
        for chunk in chunks:
            if not chunk: continue
            # Extract embedding
            emb_list = self.llm.create_embedding(chunk)['data']['embedding']
            embeddings.append(np.array(emb_list))
            
        if not embeddings:
            return None

        # Mean Pool: Find the "center of gravity" of the concept
        concept_vector = np.mean(embeddings, axis=0)
        
        # Normalize to unit length
        norm = np.linalg.norm(concept_vector)
        if norm > 0:
            concept_vector = concept_vector / norm
            
        return concept_vector

    def construct_analytic_lora_gguf(self, concept_vector: np.ndarray, rank=4, alpha=16):
        """
        Analytic Weight Steering:
        Constructs a valid GGUF LoRA adapter mathematically.
        It projects the concept vector onto the model's Value (v) and Output (o) projection matrices.
        """
        logger.info(f"Synthesizing Analytic LoRA (Rank {rank})...")
        
        adapter_name = "genesis_graft"
        save_path = os.path.join(self.output_dir, f"{adapter_name}.gguf")
        
        # Dimensions
        dim = concept_vector.shape
        
        # --- Mathematical Construction ---
        # Matrix B (up-proj): The Concept Vector repeated 'rank' times.
        # Shape: [dim, rank] -> Flattened for GGUF
        # We bias the model outputs towards this vector.
        lora_b_np = np.tile(concept_vector, (rank, 1)).astype(np.float32)
        
        # Matrix A (down-proj): Identity-like projection (Trigger).
        # Shape: [rank, dim]
        lora_a_np = np.zeros((rank, dim), dtype=np.float32)
        # Create a sparse identity to distribute effect
        for r in range(rank):
            lora_a_np[r, r % dim] = 1.0
            
        # Scale weights according to LoRA alpha
        scaling = alpha / rank
        lora_b_np = lora_b_np * scaling

        # --- GGUF Writer ---
        gw = gguf.GGUFWriter(save_path, "llama")
        
        # Metadata
        gw.add_string("general.architecture", "llama")
        gw.add_string("general.name", "Genesis-Analytic-Adapter")
        gw.add_uint32("adapter.lora.alpha", alpha)
        
        # Layer Targeting (Middle layers 10-20 for Knowledge Injection)
        # We assume a standard Llama structure. 
        # Ideally, we would inspect self.llm to find exact layer count, but 32 is standard for 7B.
        target_layers = range(10, 22) 
        
        for i in target_layers:
            # Llama 2/3 GGUF Tensor Naming Convention
            # blk.N.attn_v.weight.lora_a
            
            # Target v_proj (Value)
            gw.add_tensor(f"blk.{i}.attn_v.weight.lora_a", lora_a_np)
            gw.add_tensor(f"blk.{i}.attn_v.weight.lora_b", lora_b_np)
            
            # Target attn_output (Output)
            gw.add_tensor(f"blk.{i}.attn_output.weight.lora_a", lora_a_np)
            gw.add_tensor(f"blk.{i}.attn_output.weight.lora_b", lora_b_np)

        gw.write_header_to_file()
        gw.write_kv_data_to_file()
        gw.write_tensors_to_file()
        gw.close()
        
        logger.info(f"Analytic Graft Saved: {save_path}")
        return save_path

    def get_inference_model(self, adapter_path):
        """
        Returns a chat-ready Llama instance with the adapter loaded.
        """
        from llama_cpp import Llama
        
        # Re-init model with lora_path
        # Use n_threads to optimize for i7 CPU
        model = Llama(
            model_path=self.model_path,
            n_ctx=4096,
            n_gpu_layers=0, # CPU Mode
            verbose=False,
            lora_path=adapter_path, # Load the analytic graft
            n_threads=8             # Optimize for i7-4771 (4 core / 8 thread)
        )
        return model
