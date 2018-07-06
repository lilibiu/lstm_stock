# lstm_stock

#project structure
--./data: includes 2 files, one for train model and the other for test
--./model: model saved every 100 steps when training, can be used when test
--train.py: the train model program
--model.py: lstm-model file
--preprogress.py: to generate data for training and testing
--prediction.py: test file using model generated by train.py