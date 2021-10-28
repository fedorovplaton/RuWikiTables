from model.DataSetGenerator import DataSetGenerator
from my_types.Filter import Filter

ffilter = Filter()
generator = DataSetGenerator(ffilter)
generator.generate('test')
