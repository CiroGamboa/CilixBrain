//{% import imp; imp.load_source("medidorDistancia","C:\Cilix\cilixvenv\CilixBrain\cube_locator\medidorDistancia6") %};

// Importar el vector de angulos y distancias
var gr = document.getElementById('grafo');
var array = gr.getAttribute("data-cubes"); // Lista con angulos y distancias [ [angulo,distancia],[ang,dist], ...]
var rutaS = gr.getAttribute("data-ruta");
var g = JSON.parse(array);
var ruta = JSON.parse(rutaS);
//g = [[7.931468531468531, 23.671875], [22.462609890109892, 18.253012048192772], [33.2706447963801, 15.947368421052628], [48.02076923076923, 31.5625], [71.41908080451658, 26.578947368421108], [88.63552884615379, 14.708737864077653], [103.57253752345198, 21.04166666666669], [127.77427572427551, 15.78125]]
nodos = g.length + 1
//ruta = [0, 7, 6, 5, 4, 3, 2, 1, 8]
nod = []
nod.push({"data": {"id": 0}, "position": {"x": 0, "y": 0}});

//var out = {% medidorDistancia.prueba() %};
//console.log(out);

for (i = 0; i < nodos - 1; i++) { 
    tmp = {"id": i+1};
	if(g[i][0] <= 90)
	{
		x = g[i][1]*Math.cos(g[i][0]*Math.PI/180);
		y = g[i][1]*Math.sin(g[i][0]*Math.PI/180);
	}
	else
	{
		x = - g[i][1]*Math.cos(Math.PI- g[i][0]*Math.PI/180);
		y = g[i][1]*Math.sin(Math.PI - g[i][0]*Math.PI/180);
	}		
	data ={"data": tmp, "position":{ "x": x*100, "y": - y*100}};
	nod.push(data);
}
//{ data: { id: 'ab', weight: 2, source: 'a', target: 'b' }
edg = []
for (i = 0; i < nodos; i++) {
	for (j = i + 1; j < nodos; j++) {
		tmp = {"id": String(i) + String(j), "source": i, "target": j };//"weight": ady[i][j], "source": i, "target": j };
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
        'target-arrow-shape': 'none', //sin flecha (triangle) 
        'width': 6,
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
    },

  layout: {
    name: 'preset',
    directed: true, //no dirigido
    roots: '#0',
    padding: 10
  }
});

//argumentos: raiz, fx visita, direccion segun target. 
bfs = []
for(i = 0; i < 6; i++)
{
	bfs.push(cy.elements().bfs('#' + String(i), function(){}, true));
}

//var bfs = cy.elements().bfs('#0', function(){}, true); 
//bfs.found.addClass('highlighted');
//ruta = [0, 4, 5, 3, 6, 1, 2]

cy.$('#0').css("background-color", "red");

var i = 0;
var highlightNextEle = function(){
  if(i < ruta.length)
  {
	cy.$('#' + String(ruta[i])).addClass('highlighted');
	setTimeout(highlightNextEle, 1500);
  }
  
  if(i < ruta.length - 1)
  {
	cy.$('#' + String(ruta[i]) + String(ruta[i+1])).addClass('highlighted');
	cy.$('#' + String(ruta[i + 1]) + String(ruta[i])).addClass('highlighted');
	//setTimeout(highlightNextEle, 5000);
  }
  i++;
};
highlightNextEle();
