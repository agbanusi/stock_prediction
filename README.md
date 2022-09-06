# Forex Auto Trading and Prediction App
It is built to choose from a range of algorithm, to detect changes and predict market movements and make trades for you on your behalf on forex time or meta trader.

### List of Trend Algorithm available are:
- RSI
- Bollinger Bands
- Chaikin A/D oscillator

### List of momentum Algorithm available are:
- Stochastic Gradient
- Parabolic SAR 
- MACD
- SMVA
- Momentum
- Williams %R

### List of volume indicators are:
- Money Flow Index
- On Balance Volume

### ML Algorithm are:
- Linear regression
- Logistic regression
- KNN
- trees
- random forest
- autoML with best accuracy on auto updated validation data

Currencies trades accpeted are "EURUSD","EURGBP","EURAUD","EURNZD","EURJPY","EURCHF","EURCAD",
   "GBPUSD","AUDUSD","NZDUSD","USDJPY","USDCHF","USDCAD","GBPAUD",
   "GBPNZD","GBPJPY","GBPCHF","GBPCAD","AUDJPY","CHFJPY","CADJPY",
   "AUDNZD","AUDCHF","AUDCAD","NZDJPY","NZDCHF","NZDCAD","CADCHF"

### Other features
- Whatsapp updates on opening or closing of trade by bot using twilio
- combination of ML and Algorithm Indicators to trade together and separately

## Simple webpage built with Flask
There is a simple webapp responsible for choosing the algorithms to use, four algorithms must be chosen, one from each three types of algorithms and the fourth from any, they each contribute 30% except the fourth which is 10%, a corelation of above 70% allows the bot to trade on your behalf.

To run;

Run ``` pip install requirements.txt ```

Then run ``` python3 app.py ```

Keys and secrets do not work so you have to replace them

Built on ta and Flask

You can fork and build on it especially on the UI
