"""
Python code execution engine for dynamic problem generation
"""
import sys
import io
import base64
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any, List, Tuple
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt


class CodeExecutor:
    """Safe Python code execution with namespace extraction"""
    
    # Whitelist of allowed imports
    ALLOWED_IMPORTS = {
        'numpy': 'numpy',
        'np': 'numpy',
        'matplotlib': 'matplotlib',
        'plt': 'matplotlib.pyplot',
        'math': 'math',
        'random': 'random',
        'Value': 'quizfusion.stuff',
        'Unit': 'quizfusion.stuff',
    }
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
    
    def execute(self, code: str, seed: int = None) -> Tuple[bool, Dict[str, Any], str, List[str]]:
        """
        Execute Python code and return namespace, output, and captured figures
        
        Returns:
            (success, namespace, output, figures)
            - success: bool indicating if execution succeeded
            - namespace: dict of variables defined in code
            - output: str with stdout/stderr
            - figures: list of base64-encoded PNG images
        """
        namespace = {}
        output_buffer = io.StringIO()
        figures = []
        
        try:
            # Set up the execution environment
            exec_globals = {
                '__builtins__': __builtins__,
                'print': print,  # Allow print statements
            }
            
            # Import allowed modules
            try:
                import numpy as np
                exec_globals['np'] = np
                exec_globals['numpy'] = np
                
                import math
                exec_globals['math'] = math
                
                import random
                exec_globals['random'] = random
                
                # Import quizfusion modules
                sys.path.insert(0, '/Users/mjhaas/code/QuizFusion')
                from quizfusion.stuff import Value, Unit
                exec_globals['Value'] = Value
                exec_globals['Unit'] = Unit
                
                # Set random seed if provided
                if seed is not None:
                    np.random.seed(seed)
                    random.seed(seed)
                
            except ImportError as e:
                return False, {}, f"Import error: {str(e)}", []
            
            # Capture stdout/stderr
            with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
                # Execute the code
                exec(code, exec_globals, namespace)
                
                # Capture any matplotlib figures
                figures = self._capture_figures()
            
            # Filter namespace to only include user-defined variables
            filtered_namespace = {
                k: v for k, v in namespace.items()
                if not k.startswith('_') and k not in ['print', 'plt', 'np', 'numpy', 'math', 'random']
            }
            
            # Convert Value objects to serializable format
            serializable_namespace = self._serialize_namespace(filtered_namespace)
            
            output = output_buffer.getvalue()
            return True, serializable_namespace, output, figures
            
        except Exception as e:
            error_output = output_buffer.getvalue()
            error_msg = f"{error_output}\nError: {type(e).__name__}: {str(e)}"
            return False, {}, error_msg, []
    
    def _capture_figures(self) -> List[str]:
        """Capture all open matplotlib figures as base64-encoded PNG images"""
        figures = []
        for fig_num in plt.get_fignums():
            fig = plt.figure(fig_num)
            
            # Save figure to bytes buffer
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            
            # Encode as base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            figures.append(img_base64)
            
            plt.close(fig)
        
        return figures
    
    def _serialize_namespace(self, namespace: Dict[str, Any]) -> Dict[str, Any]:
        """Convert namespace to JSON-serializable format"""
        serialized = {}
        
        for key, value in namespace.items():
            try:
                # Check if it's a Value object
                if hasattr(value, 'magnitude') and hasattr(value, 'units'):
                    serialized[key] = {
                        '_type': 'Value',
                        'magnitude': float(value.magnitude),
                        'units': str(value.units),
                        'formatted': str(value)
                    }
                # Handle numpy types
                elif hasattr(value, 'item'):  # numpy scalar
                    serialized[key] = value.item()
                # Handle basic types
                elif isinstance(value, (int, float, str, bool, list, dict)):
                    serialized[key] = value
                else:
                    # For other types, store the string representation
                    serialized[key] = {
                        '_type': type(value).__name__,
                        'repr': str(value)
                    }
            except Exception as e:
                # If serialization fails, store error info
                serialized[key] = {
                    '_type': 'SerializationError',
                    'error': str(e)
                }
        
        return serialized


def substitute_variables(template: str, namespace: Dict[str, Any]) -> str:
    """
    Substitute variables in template string using namespace
    
    Supports formats like:
    - {variable_name}
    - {variable_name:.2f}
    """
    result = template
    
    for key, value in namespace.items():
        # Handle Value objects
        if isinstance(value, dict) and value.get('_type') == 'Value':
            formatted = value.get('formatted', str(value))
            result = result.replace(f"{{{key}}}", formatted)
        else:
            # Replace simple placeholders
            result = result.replace(f"{{{key}}}", str(value))
    
    # TODO: Handle format specifiers like {variable:.2f}
    # This would require more sophisticated parsing
    
    return result
