# Alpha Zero Program for Quoridor

This is a Alpha Zero program for quoridor. If you aren't familiar to quoridor, chech [this](https://en.wikipedia.org/wiki/Quoridor) out.

This repository's network is not trained because it needs realy long time and enough computer resources. Unfortunately I am a poor student and have neither of them.
So, if you have them, train this network instead of me. That would be vary thankful.

![Board]

## Environment

| | Version |
| ------ | ------ |
| Python | 3.8.11 |
| tensorflow | 2.4.1 |
| Flask | 1.1.2 |
| Flask-RESTful | 0.3.8 |
| Vue-CLI | 4.5.13 |
| Vue.js | 2.6.14 |
| Vuex | 3.6.2 |
| axios | 0.21.1 |

## Tech

I introduced some open source frameworks blow.

- [Vue.js] - Frontend framework for single page application.
- [Flask] - Server side framefork.
- [tensorflow] - Deep neural network framework for alpha zero.
- Asynchronous processing - Used axios.

## Installation

Clone this repository and isntall packages you need.

```sh
git clone git@github.com:nakanoi/QuoridorAlphaZero.git
pip install tensorflow flask
```

## Match

With the assumption, you have to done installation avobe.
This network is **not trained**. So that you can win really easy.
This application sends **axios post** to server and get response.
1. Build Vue application & flask server. And go the [application page].
```sh
cd QuoridorAlphaZero/match
npm run build
cd ../prediction
python flask_quoridor.py
```
2. Select you move first or second.
![select]
3. In your turn, you can move your pawn to one of the grids which have lightgreen circle. After click it, it will be red and show the context 'Next'.
Or, you can block gap between grids where is dark blue when you hover it. After click it, it will be green wall.
![move]![hover]![block]
4. Click 'Send Action' button. This would take a while because of network prediction. Repeat over 3&4 until this match is over.

## Train Network

1. Remove network's weight. When you want to build or train new model, you should do this.
```sh
cd QuoridorAlphaZero/quoridor
rm -r networks
```
2. Run train script. When you want to run on [jupyter notebook] environment or [google colaboratory], run ```train.ipynb``` file.
```sh
python train.py
```

## Tips
1. When you want to change Quoridor's environment, which is wall's number or board's size, change blow. This repository's values are the same as original Quoridor rule.
```python
# quoridor/config.py
LENGTH = 9 # Board's length.
WALLS = 10 # Wall's number you have at first.
```
```javascript
// match/src/components/match.vue
export default {
  // ...
  data () {
      // ...
      len: 9,
      walls: 10
    }
  // ...
  },
```
2. When you want to change Alpha Zero's hyper paramators like train epoch, change ```config.py```'s variables.

## Reference
- ALpha Zero [paper link].

## License

MIT

**Thank you for seeing my repository.**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
   [Vue.js]: <https://vuejs.org/index.html>
   [Flask]: <https://flask.palletsprojects.com/en/2.0.x/>
   [tensorflow]: <https://www.tensorflow.org/>
   [Board]: <https://user-images.githubusercontent.com/72122101/131285762-12d71adb-043d-4809-a5fc-5906ba487cbd.png>
   [select]: <https://user-images.githubusercontent.com/72122101/131286335-b7c8ae37-a5f7-44df-ab65-f7fa8be5b335.png>
   [move]: <https://user-images.githubusercontent.com/72122101/131286915-f80e2b52-722b-4ee0-8c73-7c817df21b61.png>
   [hover]: <https://user-images.githubusercontent.com/72122101/131286676-eb1791be-3f76-4e84-8374-7952a3030623.png>
   [block]: <https://user-images.githubusercontent.com/72122101/131286810-c6a0bed6-b2d0-44af-8e89-dea8b14c6457.png>
   [application page]: <http://127.0.0.1:5000/>
   [jupyter notebook]: <https://jupyter.org/>
   [google colaboratory]: <https://colab.research.google.com/>
   [paper link]: <https://arxiv.org/pdf/1712.01815.pdf>