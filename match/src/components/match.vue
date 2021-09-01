<template>
  <div>
    <div v-if="selectFirstSecond">
      <div>
        <p>Select You Are</p>
        <button @click="firstSecond(false)" class="firstsecond first">First</button>
        <p>or</p>
        <button @click="firstSecond(true)" class="firstsecond second">Second</button>
      </div>
    </div>
    <div v-else-if="loading">
      <h2>loading....</h2>
    </div>
    <div v-else>
      <div id="draw-wrap">
        <div class="own-wrap own-wrap-self">
          <p class="own-text">WALLS YOU HAVE</p>
          <div id="walls_other" class="own_walls walls_self">
            <div v-for="a in boards.board.walls_self" v-bind:key="a" class="own own_self"></div>
            <div v-for="b in boards.walls - boards.board.walls_self" v-bind:key="b" class="own own_self own_transepose"></div>
          </div>
        </div>
        <div id="draw">
          <div v-for="i in boards.len" v-bind:key="i" class="row-wrap">
            <div class="row row-top">
              <div v-for="j in boards.len" v-bind:key="j">
                <div @click="pawnClick((i - 1) * boards.len + (j - 1))" class="grid"></div>

                <div v-if="i != len && j != boards.len && boards.board.takables.includes(8 + (i - 1) * (boards.len - 1) + (j - 1))"
                  v-on:mouseover="wallOver(8 + (i - 1) * (boards.len - 1) + (j - 1), true)"
                  v-on:mouseleave="wallLeave(8 + (i - 1) * (boards.len - 1) + (j - 1), true)"
                  @click="wallClick(8 + (i - 1) * (boards.len - 1) + (j - 1), true)"
                  class="wall wall_v"></div>
                <div v-else-if="i != boards.len && j != boards.len" class="wall wall_v"></div>
                <div v-else-if="i == boards.len && j != boards.len" class="wall wall_v"></div>
              </div>
            </div>
            <div class="row row-bottom">
              <div v-for="k in boards.len" v-bind:key="k">
                <div v-if="i != boards.len && k != boards.len && boards.board.takables.includes(8 + (boards.len - 1) * (boards.len - 1) + (i - 1) * (boards.len - 1) + (k - 1))"
                  v-on:mouseover="wallOver(8 + (boards.len - 1) * boards.len + (i - 1) * boards.len + (k - 1), false)"
                  v-on:mouseleave="wallLeave(8 + (boards.len - 1) * boards.len + (i - 1) * boards.len + (k - 1), false)"
                  @click="wallClick(8 + (boards.len - 1) ** 2 + (i - 1) * (boards.len - 1) + (k - 1), false)"
                  class="wall wall_h"></div>
                <div v-else-if="i != boards.len && k != boards.len" class="wall wall_h"></div>
                <div v-else-if="i != boards.len" class="wall wall_h"></div>

                <div v-if="i != boards.len && k != boards.len" class="blank" open="0"></div>
              </div>
            </div>
          </div>
        </div>
        <div class="own-wrap own-wrap-other">
          <div id="walls_self" class="own_walls walls_other">
            <div v-for="c in boards.walls - boards.board.walls_other" v-bind:key="c" class="own own_other own_transepose"></div>
            <div v-for="d in boards.board.walls_other" v-bind:key="d" class="own own_other"></div>
          </div>
          <p class="own-text">WALLS NETWORK HAS</p>
        </div>
      </div>
      <p v-if="isWin" class="result result-win">You Win.</p>
      <p v-else-if="isLose" class="result result-lose">You Lose.</p>
      <button v-if="isOver"><a href="http://127.0.0.1:5000">Rematch</a></button>
      <button v-else-if="'take_action' in boards.board" @click="getBoard()" class="confirm">Send Action</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Board',
  data: function () {
    return {
      boards: {
        'board': null,
        'oldBoard': null,
        'net': null,
        'len': 9,
        'walls': 10
      }
    }
  },
  methods: {
    drawBoard () {
      var i = 0
      var j = 0
      var act = 0
      var pawns = document.getElementsByClassName('grid')
      var wallVs = document.getElementsByClassName('wall_v')
      var wallHs = document.getElementsByClassName('wall_h')
      const moves = [[1, 0], [0, 1], [-1, 0], [0, -1]]

      for (i = 0; i < this.boards.len; i++) {
        for (j = 0; j < this.boards.len; j++) {
          // pawn position
          var pawn = pawns[i * this.boards.len + j]
          pawn.setAttribute('pawn', i * this.boards.len + j)
          if (this.boards.board['pawn_self']['position'][0] === i && this.boards.board['pawn_self']['position'][1] === j) {
            pawn.setAttribute('exists', 'self')
          } else if (this.boards.board['pawn_other_position'][0] === i && this.boards.board['pawn_other_position'][1] === j) {
            pawn.setAttribute('exists', 'other')
          } else {
            var movable = false
            // takable actions
            if (this.boards.board['over'] === false) {
              for (var k = 0; k < this.boards.board['takables'].length; k++) {
                for (var l = 0; l < 4; l++) {
                  if (this.boards.board['takables'][k] === l) {
                    if (this.boards.board['pawn_self']['position'][0] + moves[l][0] === i && this.boards.board['pawn_self']['position'][1] + moves[l][1] === j) {
                      pawn.setAttribute('exists', 'possible')
                      pawn.setAttribute('action', l)
                      movable = true
                      break
                    }
                  } else if (this.boards.board['takables'][k] === l + 4) {
                    if (this.boards.board['pawn_other_position'][0] + moves[l][0] === i && this.boards.board['pawn_other_position'][1] + moves[l][1] === j) {
                      pawn.setAttribute('exists', 'possible')
                      pawn.setAttribute('action', l + 4)
                      movable = true
                      break
                    }
                  }
                }
              }
            }
            if (movable === false) {
              pawn.setAttribute('exists', '')
            }
          }

          if (j !== this.boards.len - 1 && this.boards.board['over'] === false) {
            // wall vertical
            var wallV = wallVs[i * (this.boards.len - 1) + j]
            wallV.setAttribute('open_vertical', i * (this.boards.len - 1) + j)
            wallV.setAttribute('open', this.boards.board['wall_vertical']['open_vertical'][i][j])
            wallV.setAttribute('hover', 8 + i * (this.boards.len - 1) + j)
            act = 8 + i * (this.boards.len - 1) + j
            if (i !== this.boards.len - 1 && this.boards.board['wall_vertical']['open_vertical'][i][j] === 1 && this.boards.board['takables'].includes(act)) {
              wallV.setAttribute('action', act)
            }
          }
        }

        if (i !== this.boards.len - 1 && this.boards.board['over'] === false) {
          for (j = 0; j < this.boards.len; j++) {
            // wall horizontal
            var wallH = wallHs[i * this.boards.len + j]
            wallH.setAttribute('open_horizontal', i * this.boards.len + j)
            wallH.setAttribute('open', this.boards.board['wall_horizontal']['open_horizontal'][i][j])
            wallH.setAttribute('hover', 8 + (this.boards.len - 1) * this.boards.len + i * this.boards.len + j)
            act = 8 + (this.boards.len - 1) * (this.boards.len - 1) + i * (this.boards.len - 1) + j
            if (j !== this.boards.len - 1 && this.boards.board['wall_horizontal']['open_horizontal'][i][j] === 1 && this.boards.board['takables'].includes(act)) {
              wallH.setAttribute('action', act)
            }
          }
        }
      }
    },
    async getAPI () {
      this.cleanSelected()
      const path = `http://127.0.0.1:5000/api/action`
      this.$set(this.boards, 'oldBoard', this.boards.board)
      if (this.boards.oldBoard === null) {
        this.$set(this.boards, 'oldBoard', {'network_first': this.boards['net']})
      }
      this.boards.board = null
      const res = await axios.post(path, this.boards.oldBoard)
        .then(response => {
          this.$set(this.boards, 'board', JSON.parse(response.data))
        })
        .catch(error => {
          console.log(error)
        })
      this.$nextTick(() => {
        this.drawBoard()
      })
      return res
    },
    getBoard () {
      this.getAPI()
    },
    firstSecond (first) {
      if (first === true) {
        this.$set(this.boards, 'net', true)
        this.getBoard()
      } else {
        this.$set(this.boards, 'net', false)
        this.getBoard()
      }
    },
    wallOver (hover, vertical) {
      var wallTop = document.querySelector('div[hover="' + String(hover) + '"]')
      var wallBottom = null

      if (vertical === true) {
        wallBottom = document.querySelector('div[hover="' + String(hover + this.boards.len - 1) + '"]')
      } else {
        wallBottom = document.querySelector('div[hover="' + String(hover + 1) + '"]')
      }

      wallTop.classList.add('wall-hover')
      wallBottom.classList.add('wall-hover')
    },
    wallLeave (hover, vertical) {
      var wallTop = document.querySelector('div[hover="' + String(hover) + '"]')
      var wallBottom = null

      if (vertical === true) {
        wallBottom = document.querySelector('div[hover="' + String(hover + this.boards.len - 1) + '"]')
      } else {
        wallBottom = document.querySelector('div[hover="' + String(hover + 1) + '"]')
      }
      wallTop.classList.remove('wall-hover')
      wallBottom.classList.remove('wall-hover')
    },
    cleanSelected () {
      var selected = document.querySelector('div.pawn-selected')
      if (selected !== null) {
        selected.classList.remove('pawn-selected')
      }

      selected = document.querySelectorAll('div.wall-selected')
      for (var i = 0; i < selected.length; i++) {
        selected[i].classList.remove('wall-selected')
      }
    },
    pawnClick (pawnIdx) {
      var pawn = document.querySelector('div[pawn="' + String(pawnIdx) + '"]')
      if (pawn.hasAttribute('action')) {
        this.cleanSelected()
        var action = pawn.getAttribute('action')
        pawn.classList.add('pawn-selected')

        this.$set(this.boards.board, 'take_action', Number(action))
      }
    },
    wallClick (action, vertical) {
      this.cleanSelected()

      var clickedWall = document.querySelector('div[action="' + String(action) + '"]')
      var hover = clickedWall.getAttribute('hover')
      var clickedWallBottom = document.querySelector('div[hover="' + String(Number(hover) + 1) + '"]')
      if (vertical === true) {
        clickedWallBottom = document.querySelector('div[hover="' + String(Number(hover) + this.boards.len - 1) + '"]')
      }

      clickedWall.classList.add('wall-selected')
      clickedWallBottom.classList.add('wall-selected')
      this.$set(this.boards.board, 'take_action', Number(action))
    }
  },
  computed: {
    selectFirstSecond: function () {
      return this.boards.board === null && this.boards.net == null
    },
    loading: function () {
      return this.boards.board === null
    },
    isWin: function () {
      return this.boards.board.over === true && this.boards.board.point === 1
    },
    isLose: function () {
      return this.boards.board.over === true && this.boards.board.point === 0
    },
    isOver: function () {
      return this.boards.board.over === true
    },
    showSelfWalls: function () {
      return this.boards.board.walls_self
    },
    showOtherWalls: function () {
      return this.boards.board.walls_other
    },
    showState: function () {
      return this.boards.board
    }
  }
}
</script>

<style>
#app {
  margin-top: 0;
}
button {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  border: 2px solid #000;
  border-radius: 0;
  background: #fff;
  padding: .5em 2em;
  font-size: 24px;
  cursor: pointer;
}
button:hover {
  color: #fff;
  background: #000;
}
.own-wrap {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  width: 250px;
}
.own-wrap-other {
  justify-content: flex-end;
}
.own-text {
  text-align: center;
  font-size: 20px;
}
#draw-wrap {
  display: flex;
  justify-content: center;
}
#draw {
  margin: 0 3em 1em;
}
.row {
  display: flex;
}
.row > div {
  display: flex;
}
.grid {
  width: 50px;
  height: 50px;
  background: #ffad8f;
  cursor: pointer;
  border-radius: 4px;
  position: relative;
}
.grid[exists='other']:after {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -webkit-transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  content: 'Network';
  width: 40px;
  height: 40px;
  border-radius: 20px;
  background: #574bc2;
}
.grid[exists='self']:after {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -webkit-transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  content: 'YOU';
  width: 40px;
  height: 40px;
  border-radius: 20px;
  background: #73db65;
}
.grid[exists='possible']:after {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -webkit-transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  content: '';
  width: 40px;
  height: 40px;
  border-radius: 20px;
  background: rgba(115, 219, 101, 0.5);
}
.pawn-selected:after {
  content: 'NEXT'!important;
  background: rgba(255, 17, 0, 0.5) !important;
}
.wall_v {
  width: 10px;
  height: 50px;
  cursor: pointer;
  border-radius: 2px;
}
.wall_h {
  width: 50px;
  height: 10px;
  cursor: pointer;
  border-radius: 2px;
}
.wall_h[open='0'], .wall_v[open='0'] {
  background: #1a110e;
  border-radius: 0;
}
.wall-hover {
  background: rgba(26, 17, 14, 0.5);
  border-radius: 0;
}
.wall-selected {
  background: rgba(32, 253, 12, 0.5);
}
.blank {
  width: 10px;
  height: 10px;
  background: #1a110e;
}
.own_walls {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}
.walls_other {
  align-items: flex-end;
}
.own {
  width: 10px;
  height: 110px;
  background: #1a110e;
  margin: 0 3px;
}
.own_transepose {
  background: transparent !important;
}
.result {
  padding: .2em 0;
  font-size: 16px;
  color: rgb(247, 20, 20);
}
.result-lose {
  color: rgb(0, 3, 192);
}
a {
  color: black;
  text-decoration: none;
}

</style>
