//var a = parent.document.URL.substring(parent.document.URL.indexOf('?'), parent.document.URL.length);
//v = a[a.length-1];

function getNumber(v)
{
	document.getElementById('vid').src = '/static/contenido/track_' + v + 'cubos.mp4';//'contenido/track_' + v + 'cubos.mp4';
	document.getElementById('origin').src = '/static/contenido/img1-' + v + 'cubos.jpg';//'contenido/img1-' + v + 'cubos.jpg';
	document.getElementById('hsv').src = '/static/contenido/img2-' + v + 'cubos.jpg';//'contenido/img2-' + v + 'cubos.jpg';
	document.getElementById('umbral').src = '/static/contenido/img3-' + v + 'cubos.jpg';//'contenido/img3-' +v + 'cubos.jpg';
	document.getElementById('track').src = '/static/contenido/img4-' + v + 'cubos.jpg';//'contenido/img4-' + v + 'cubos.jpg';
};

function getInfo(v)
{
	//contenido/mini-3cubos.jpg
	document.getElementById('mini').src = '/static/contenido/top-' + v + 'cubos.jpg';
}