webpackJsonp([1],{NHnr:function(t,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var a=s("/5sW"),o={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"app"}},[e("router-view")],1)},staticRenderFns:[]};var l=s("VU/8")({name:"App"},o,!1,function(t){s("gsu9")},null,null).exports,r=s("/ocq"),i=s("mtWM"),n=s.n(i),d={name:"Board",data:function(){return{boards:{board:null,oldBoard:null,net:!0},len:5,walls:4}},methods:{drawBoard:function(){var t=0,e=0,s=0,a=document.getElementsByClassName("grid"),o=document.getElementsByClassName("wall_v"),l=document.getElementsByClassName("wall_h"),r=[[1,0],[0,1],[-1,0],[0,-1]];for(t=0;t<this.len;t++){for(e=0;e<this.len;e++){var i=a[t*this.len+e];if(i.setAttribute("pawn",t*this.len+e),this.boards.board.pawn_self.position[0]===t&&this.boards.board.pawn_self.position[1]===e)i.setAttribute("exists","self");else if(this.boards.board.pawn_other_position[0]===t&&this.boards.board.pawn_other_position[1]===e)i.setAttribute("exists","other");else{var n=!1;if(!1===this.boards.board.over)for(var d=0;d<this.boards.board.takables.length;d++)for(var c=0;c<4;c++)if(this.boards.board.takables[d]===c){if(this.boards.board.pawn_self.position[0]+r[c][0]===t&&this.boards.board.pawn_self.position[1]+r[c][1]===e){i.setAttribute("exists","possible"),i.setAttribute("action",c),n=!0;break}}else if(this.boards.board.takables[d]===c+4&&this.boards.board.pawn_other_position[0]+r[c][0]===t&&this.boards.board.pawn_other_position[1]+r[c][1]===e){i.setAttribute("exists","possible"),i.setAttribute("action",c+4),n=!0;break}!1===n&&i.setAttribute("exists","")}if(e!==this.len-1&&!1===this.boards.board.over){var u=o[t*(this.len-1)+e];u.setAttribute("open_vertical",t*(this.len-1)+e),u.setAttribute("open",this.boards.board.wall_vertical.open_vertical[t][e]),u.setAttribute("hover",8+t*(this.len-1)+e),s=8+t*(this.len-1)+e,t!==this.len-1&&1===this.boards.board.wall_vertical.open_vertical[t][e]&&this.boards.board.takables.includes(s)&&u.setAttribute("action",s)}}if(t!==this.len-1&&!1===this.boards.board.over)for(e=0;e<this.len;e++){var v=l[t*this.len+e];v.setAttribute("open_horizontal",t*this.len+e),v.setAttribute("open",this.boards.board.wall_horizontal.open_horizontal[t][e]),v.setAttribute("hover",8+(this.len-1)*this.len+t*this.len+e),s=8+(this.len-1)*(this.len-1)+t*(this.len-1)+e,e!==this.len-1&&1===this.boards.board.wall_horizontal.open_horizontal[t][e]&&this.boards.board.takables.includes(s)&&v.setAttribute("action",s)}}},getBoard:function(){var t=this;this.cleanSelected();this.$set(this.boards,"oldBoard",this.boards.board),null===this.boards.oldBoard&&this.$set(this.boards,"oldBoard",{network_first:this.boards.net}),n.a.post("http://127.0.0.1:5000/api/action",this.boards.oldBoard).then(function(e){console.log(e.data),t.$set(t.boards,"board",e.data),t.drawBoard()}).catch(function(t){console.log(t)})},firstSecond:function(t){!0===t?(this.$set(this.boards,"net",!0),this.getBoard()):(this.$set(this.boards,"net",!1),this.getBoard())},wallOver:function(t,e){var s=document.querySelector('div[hover="'+String(t)+'"]'),a=null;a=!0===e?document.querySelector('div[hover="'+String(t+this.len-1)+'"]'):document.querySelector('div[hover="'+String(t+1)+'"]'),s.classList.add("wall-hover"),a.classList.add("wall-hover")},wallLeave:function(t,e){var s=document.querySelector('div[hover="'+String(t)+'"]'),a=null;a=!0===e?document.querySelector('div[hover="'+String(t+this.len-1)+'"]'):document.querySelector('div[hover="'+String(t+1)+'"]'),s.classList.remove("wall-hover"),a.classList.remove("wall-hover")},cleanSelected:function(){var t=document.querySelector("div.pawn-selected");null!==t&&t.classList.remove("pawn-selected"),t=document.querySelectorAll("div.wall-selected");for(var e=0;e<t.length;e++)t[e].classList.remove("wall-selected")},pawnClick:function(t){var e=document.querySelector('div[pawn="'+String(t)+'"]');if(e.hasAttribute("action")){this.cleanSelected();var s=e.getAttribute("action");e.classList.add("pawn-selected"),this.boards.board.take_action=Number(s)}},wallClick:function(t,e){this.cleanSelected();var s=document.querySelector('div[action="'+String(t)+'"]'),a=s.getAttribute("hover"),o=document.querySelector('div[hover="'+String(Number(a)+1)+'"]');!0===e&&(o=document.querySelector('div[hover="'+String(Number(a)+this.len-1)+'"]')),s.classList.add("wall-selected"),o.classList.add("wall-selected"),this.boards.board.take_action=Number(t)}},updated:function(){this.drawBoard()}},c={render:function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[null==t.boards.board?s("div",[s("div",[s("p",[t._v("Select You Are")]),t._v(" "),s("button",{staticClass:"firstsecond first",on:{click:function(e){return t.firstSecond(!1)}}},[t._v("First")]),t._v(" "),s("p",[t._v("or")]),t._v(" "),s("button",{staticClass:"firstsecond second",on:{click:function(e){return t.firstSecond(!0)}}},[t._v("Second")])])]):s("div",[s("div",{attrs:{id:"draw-wrap"}},[s("div",{staticClass:"own-wrap own-wrap-self"},[s("p",{staticClass:"own-text"},[t._v("WALLS YOU HAVE")]),t._v(" "),s("div",{staticClass:"own_walls walls_self",attrs:{id:"walls_other"}},[t._l(t.boards.board.splice().walls_self,function(t){return s("div",{key:t,staticClass:"own own_other"})}),t._v(" "),t._l(t.walls-t.boards.board.splice().walls_self,function(t){return s("div",{key:t,staticClass:"own own_other own_transepose"})})],2)]),t._v(" "),s("div",{attrs:{id:"draw"}},t._l(t.len,function(e){return s("div",{key:e,staticClass:"row-wrap"},[s("div",{staticClass:"row row-top"},t._l(t.len,function(a){return s("div",{key:a},[s("div",{staticClass:"grid",on:{click:function(s){t.pawnClick((e-1)*t.len+(a-1))}}}),t._v(" "),e!=t.len&&a!=t.len&&t.boards.board.splice().takables.includes(8+(e-1)*(t.len-1)+(a-1))?s("div",{staticClass:"wall wall_v",on:{mouseover:function(s){t.wallOver(8+(e-1)*(t.len-1)+(a-1),!0)},mouseleave:function(s){t.wallLeave(8+(e-1)*(t.len-1)+(a-1),!0)},click:function(s){t.wallClick(8+(e-1)*(t.len-1)+(a-1),!0)}}}):e!=t.len&&a!=t.len?s("div",{staticClass:"wall wall_v"}):e==t.len&&a!=t.len?s("div",{staticClass:"wall wall_v"}):t._e()])}),0),t._v(" "),s("div",{staticClass:"row row-bottom"},t._l(t.len,function(a){return s("div",{key:a},[e!=t.len&&a!=t.len&&t.boards.board.splice().takables.includes(8+Math.pow(t.len-1,2)+(e-1)*(t.len-1)+(a-1))?s("div",{staticClass:"wall wall_h",on:{mouseover:function(s){t.wallOver(8+(t.len-1)*t.len+(e-1)*t.len+(a-1),!1)},mouseleave:function(s){t.wallLeave(8+(t.len-1)*t.len+(e-1)*t.len+(a-1),!1)},click:function(s){t.wallClick(8+Math.pow(t.len-1,2)+(e-1)*(t.len-1)+(a-1),!1)}}}):e!=t.len&&a!=t.len?s("div",{staticClass:"wall wall_h"}):e!=t.len?s("div",{staticClass:"wall wall_h"}):t._e(),t._v(" "),e!=t.len&&a!=t.len?s("div",{staticClass:"blank",attrs:{open:"0"}}):t._e()])}),0)])}),0),t._v(" "),s("div",{staticClass:"own-wrap own-wrap-other"},[s("div",{staticClass:"own_walls walls_other",attrs:{id:"walls_self"}},[t._l(t.walls-t.boards.board.splice().walls_other,function(t){return s("div",{key:t,staticClass:"own own_other own_transepose"})}),t._v(" "),t._l(t.boards.board.splice().walls_other,function(t){return s("div",{key:t,staticClass:"own own_other"})})],2),t._v(" "),s("p",{staticClass:"own-text"},[t._v("WALLS NETWORK HAS")])])]),t._v(" "),1==t.boards.board.splice().over&&1==t.boards.board.splice().point?s("p",{staticClass:"result result-win"},[t._v("You Win.")]):1==t.boards.board.splice().over&&0==t.boards.board.splice().point?s("p",{staticClass:"result result-lose"},[t._v("You Lose.")]):t._e(),t._v(" "),1==t.boards.board.splice().over?s("button",[s("a",{attrs:{href:"http://127.0.0.1:5000"}},[t._v("Rematch")])]):s("button",{staticClass:"confirm",on:{click:function(e){return t.getBoard()}}},[t._v("Send Action")])])])},staticRenderFns:[]};var u=s("VU/8")(d,c,!1,function(t){s("p3KM")},null,null).exports;a.a.use(r.a);var v=new r.a({mode:"history",routes:[{path:"/",name:"Match",component:u}]});a.a.config.productionTip=!1,new a.a({el:"#app",router:v,render:function(t){return t(l)}})},gsu9:function(t,e){},p3KM:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.f3184df2f35891d87234.js.map