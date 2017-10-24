
function grafo(g, ruta)
{
  nodos = g.length + 1
  //g = [[34,3.61],[55,7.21], [90,3], [116,4.47], [134,4.24], [153,4.47]]
  //ruta = [0, 6, 5, 4, 3, 1, 2]
  nod = []
  nod.push({"data": {"id": 0}, "position": {"x": 0, "y": 0}});


  for (i = 0; i < nodos - 1; i++) { 
    tmp = {"id": i+1};
    g[i][0] = Math.PI - g[i][0];
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
    data ={"data": tmp, "position":{ "x": - x*100, "y": y*100}};
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
      'content': 'data(id)',
      'width': 150,
      'height': 150,
      'font-size': 80
      })
    .selector('edge')
      .css({
      'curve-style': 'bezier',
      'target-arrow-shape': 'none', //sin flecha (triangle) 
      'width': 10,
      'line-color': '#ddd',
      'target-arrow-color': '#ddd'
      })
    .selector('.highlighted')
      .css({
      'background-color': '#ff0000',//'#61bffc',
      'line-color': '#ff0000',//'#61bffc',
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
    },
    
    zoom: 0.2,
    pan: { x: 0, y: 0 },
    
    zoomingEnabled: true,
    userZoomingEnabled: false,
    panningEnabled: true,
    userPanningEnabled: false,
    boxSelectionEnabled: false,
    selectionType: 'single',
    touchTapThreshold: 8,
    desktopTapThreshold: 4,
    autolock: false,
    autoungrabify: false,
    autounselectify: false,

    // rendering options:
    headless: false,
    styleEnabled: true,
    hideEdgesOnViewport: false,
    hideLabelsOnViewport: false,
    textureOnViewport: false,
    motionBlur: false,
    motionBlurOpacity: 0.2,
    wheelSensitivity: 1,
    pixelRatio: 'auto'
    
    
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


  var i = 0;
  var highlightNextEle = function(){
    if(i < ruta.length)
    {
    cy.$('#' + String(ruta[i])).addClass('highlighted');
    setTimeout(highlightNextEle, 1000);
    }
    
    if(i < ruta.length - 1)
    {
    cy.$('#' + String(ruta[i]) + String(ruta[i+1])).addClass('highlighted');
    cy.$('#' + String(ruta[i + 1]) + String(ruta[i])).addClass('highlighted');
    //setTimeout(highlightNextEle, 5000);
    }
    i++;
  };

  cy.$('#0').css("background-color","black");
  /*cy.$('#0').css("width",200);
  cy.$('#0').css("height",200);*/
  highlightNextEle();
}