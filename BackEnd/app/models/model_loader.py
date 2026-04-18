import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class ModelLoader:
    """Handles loading and inference with the AI model from local folder"""
    
    @staticmethod
    def detect_device() -> str:
        """
        Auto-detect available device (GPU or CPU)
        
        Returns:
            Device string: "cuda" if GPU available, else "cpu"
        """
        if torch.cuda.is_available():
            device = "cuda"
            logger.info(f"GPU detected: {torch.cuda.get_device_name(0)}")
            logger.info(f"CUDA version: {torch.version.cuda}")
        else:
            device = "cpu"
            logger.info("No GPU detected, using CPU")
        
        return device
    
    @staticmethod
    def validate_model_folder(model_folder: str) -> bool:
        """
        Validate if model folder exists and contains required files
        
        Args:
            model_folder: Path to model folder
            
        Returns:
            True if valid, False otherwise
        """
        model_path = Path(model_folder)
        
        if not model_path.exists():
            logger.error(f"Model folder not found: {model_folder}")
            return False
        
        # Check for required files
        required_files = [
            "config.json",
            "pytorch_model.bin" or "model.safetensors"
        ]
        
        config_exists = (model_path / "config.json").exists()
        model_exists = (model_path / "pytorch_model.bin").exists() or \
                      (model_path / "model.safetensors").exists()
        
        if not config_exists:
            logger.error(f"config.json not found in {model_folder}")
            return False
        
        if not model_exists:
            logger.error(f"Model file (pytorch_model.bin or model.safetensors) not found in {model_folder}")
            return False
        
        logger.info(f"Model folder validation passed: {model_folder}")
        return True
    
    @staticmethod
    def load_model(model_folder: str, device: str = None):
        """
        Load tokenizer and model from local folder
        
        Args:
            model_folder: Path to fine-tuned model folder
            device: Device to load model on (auto-detect if None)
            
        Returns:
            Tuple of (tokenizer, model, device) or (None, None, device) if failed
            
        Raises:
            ValueError: If model folder validation fails
        """
        try:
            # Validate model folder
            if not ModelLoader.validate_model_folder(model_folder):
                raise ValueError(f"Invalid model folder: {model_folder}")
            
            # Auto-detect device if not specified
            if device is None:
                device = ModelLoader.detect_device()
            
            logger.info(f"Loading model from: {model_folder}")
            logger.info(f"Using device: {device}")
            
            # Load tokenizer
            logger.info("Loading tokenizer...")
            tokenizer = AutoTokenizer.from_pretrained(model_folder)
            
            # Set pad token if not set
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
                logger.info("Pad token set to EOS token")
            
            # Load model
            logger.info("Loading model...")
            model = AutoModelForCausalLM.from_pretrained(
                model_folder,
                torch_dtype=torch.float32 if device == "cpu" else torch.float16
            )
            model.to(device)
            model.eval()
            
            logger.info("✅ Model and tokenizer loaded successfully!")
            return tokenizer, model, device
        
        except FileNotFoundError as e:
            logger.error(f"Model files not found: {str(e)}")
            raise ValueError(f"Model files not found in {model_folder}") from e
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    @staticmethod
    def generate_story(tokenizer, model, prompt: str, max_length: int = 200, device: str = "cpu") -> str:
        """
        Generate story based on prompt
        
        Args:
            tokenizer: Loaded tokenizer
            model: Loaded model
            prompt: Input prompt for story generation
            max_length: Maximum length of generated text (including prompt)
            device: Device to use for inference
            
        Returns:
            Generated story text
        """
        if model is None or tokenizer is None:
            raise ValueError("Model or tokenizer not loaded")
        
        try:
            # Encode input
            input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
            
            logger.info(f"Generating story with max_length={max_length}")
            
            # Generate with torch.no_grad for inference
            with torch.no_grad():
                output = model.generate(
                    input_ids,
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id
                )
            
            # Decode output
            story = tokenizer.decode(output[0], skip_special_tokens=True)
            return story
        
        except Exception as e:
            logger.error(f"Error during inference: {str(e)}")
            raise

