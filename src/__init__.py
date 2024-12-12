from .base_processor import BaseProcessor
from .cpu_single import SingleCPUProcessor
from .cpu_multithread import MultiCPUProcessor
#from .spark_processor import Spark

__all__ = [
    'BaseProcessor',
    'SingleCPUProcessor',
    'MultiCPUProcessor',
    'Spark',
]