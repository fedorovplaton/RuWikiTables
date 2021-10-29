from model.DataSetGenerator import DataSetGenerator
from my_types.Filter import Filter

ffilter = Filter(
    min_cols=1,
    max_cols=1,
    min_rows=1,
    max_rows=1
)
generator = DataSetGenerator(ffilter, 'test')
generator.start()
print("")
