nodos = 7;
camino = [0, 6, 8, 7, 3, 1, 2, 5, 4];
ady = [[0, 3.61, 7.21, 3, 4.47, 4.24, 4.47], [3.61, 0, 6.380977613272764, 3.997003984913176, 5.546819396892034, 5.80238127553172, 6.390322949509599], [7.21, 6.380977613272764, 0, 6.577677499089561, 7.5060120031856385, 8.008033009905796, 8.743590116131454], [3, 3.997003984913176, 6.577677499089561, 0, 4.114373808871548, 4.222274001020345, 4.7846512306011055], [4.47, 5.546819396892034, 7.5060120031856385, 4.114373808871548, 0, 4.464674238727974, 4.899422796339998], [4.24, 5.80238127553172, 8.008033009905796, 4.222274001020345, 4.464674238727974, 0, 4.47641324504131], [4.47, 6.390322949509599, 8.743590116131454, 4.7846512306011055, 4.899422796339998, 4.47641324504131, 0]]
nod = []
for (i = 0; i < nodos; i++) { 
    tmp = {"id": i};
	data ={"data": tmp};//, "position":{ "x": i*50, "y": i*50}};
	nod.push(data);
}
//{ data: { id: 'ab', weight: 2, source: 'a', target: 'b' }
edg = []
for (i = 0; i < nodos; i++) {
	for (j = i + 1; j < nodos; j++) {
		tmp = {"id": String(i) + String(j), "weight": ady[i][j], "source": i, "target": j };
		dic = {"data": tmp};
		edg.push(dic);
	}
}

var cy = cytoscape({
  
  
  container: document.getElementById('cy'),

  boxSelectionEnabled: false,
  autounselectify: true,

  style: cytoscape.stylesheet()
    .selector('node')
      .css({
        'content': 'data(id)'
      })
    .selector('edge')
      .css({
        'curve-style': 'bezier',
        'target-arrow-shape': 'triangle', //sin flecha 
        'width': 4,
        'line-color': '#ddd',
        'target-arrow-color': '#ddd'
      })
    .selector('.highlighted')
      .css({
        'background-color': '#61bffc',
        'line-color': '#61bffc',
        'target-arrow-color': '#61bffc',
        'transition-property': 'background-color, line-color, target-arrow-color',
        'transition-duration': '0.5s'
      }),

  elements: {
      nodes: nod,

      edges: edg
    }/*,

  layout: {
    name: 'breadthfirst',
    directed: true, //no dirigido
    roots: '#0',
    padding: 10
  }*/
});

//argumentos: raiz, fx visita, direccion segun target.
var bfs = cy.elements().bfs('#0', function(){}, true); 

var i = 0;
/*var highlightNextEle = function(){
  if( i < bfs.path.length ){
    bfs.path[i].addClass('highlighted');

    i++;
    setTimeout(highlightNextEle, 1000);
  }
};*/

// kick off first highlight
highlightNextEle();
