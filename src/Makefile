all:
	@python -m logreg_predict ../datasets/dataset_test.csv evaluation_logs.json

lr:
	@python -m main

describe:
	@python -m data_analysis.main

histogram:
	@python -m data_visualization.histogram

scatter_plot:
	@python -m data_visualization.scatter_plot

pair_plot:
	@python -m data_visualization.pair_plot

training:
	@python -m data_visualization.training_board

.PHONY: describe histogram scatter_plot pair_plot
