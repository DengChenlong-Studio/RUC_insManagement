var gdoc = null;
var pdfcontent = "";
var nodeArray = new Array();
var pdfTextContent = "";
var nodeOffset = new Array();
var resultBox = new Array(); // can be annotated anytime.
var matchBox = new Array();
var markId = 1;
var refMap = new Map();
var pageHeight = 0;
var harray = new Array();
var haccumulate = 0;

var divList = new Array();
var canvasList = new Array();
var pageList = new Array();
var objList = new Array();
var rendering = new Array();
var zoomRatio = 1;

function Table(){
	this.left = 0;
	this.width = 0;
	this.height = 0;
	this.top = 0;
	this.page = 0;
	this.pageHeight = 0;
	this.pageWidth = 0;
}
class SimpleLinkService {
  //this.page = 0;
  //this.rotation = 0;
  //this.hash = 0;
  //this.map = new Map();
  constructor() {
    this.externalLinkTarget = null;
    this.externalLinkRel = null;
	this._page = 0;
	this._rotation = null;
	this._hash = 0;
	this._map  = new Map();
  }

  get pagesCount() {
    return gdoc._pdfInfo.numPages;
  }

  get page() {
    return this._page;
  }

  set page(value) {
	  this._page = value;
  }

  get rotation() {
    return this._rotation;
  }

  set rotation(value) {
	  this._rotation = value;
  }

  navigateTo(dest) {
	  console.log(dest);
  }

  getDestinationHash(dest) {
	  //console.log(dest);
    return '#'+dest;
  }

  getAnchorUrl(hash) {
    return '#'+hash;
  }

  setHash(hash) {
	  this.hash = hash;
  }

  executeNamedAction(action) {}

  cachePageRef(pageNum, pageRef) {
	  console.log(pageNum);
	  console.log(pageRef);
	  this.map.set(pageNum,pageRef);
  }

  isPageVisible(pageNumber) {
    return true;
  }

}
simpleLinkService = new SimpleLinkService();

function detectZoom (){ 
  var ratio = 0,
    screen = window.screen,
    ua = navigator.userAgent.toLowerCase();

   if (window.devicePixelRatio !== undefined) {
      ratio = window.devicePixelRatio;
  }
  else if (~ua.indexOf('msie')) {  
    if (screen.deviceXDPI && screen.logicalXDPI) {
      ratio = screen.deviceXDPI / screen.logicalXDPI;
    }
  }
  else if (window.outerWidth !== undefined && window.innerWidth !== undefined) {
    ratio = window.outerWidth / window.innerWidth;
  }
   
   if (ratio){
    //ratio = Math.round(ratio * 100);
  }
   
   return ratio;
};

function wheel(){

			haccumulate = 0;
			harray = new Array();
			var zr = detectZoom();
			console.log(zr/zoomRatio+"s");
			$container = document.getElementById("page-container");
			if(zr!=zoomRatio&&(zr/zoomRatio>1.1||zr/zoomRatio<0.9)){
				console.log(zr/zoomRatio);
				zoomRatio = zr;
				harray.length = 0;
				//$container = document.getElementById("page-container");
				canvasList.length = 0;
				//objList.length = 0;
				for(var i = 1;i<=gdoc._pdfInfo.numPages;i++){
					renderPDFText($container,gdoc,i,zoomRatio);
				}
				rendering.length = 0;
				rendering.push(1);
				renderCanvas($container,gdoc,1,zoomRatio);
			}
			var cmd = $("#page-container").scrollTop();
			//pageHeight = $("#pf1").height();
			var page_index = 0;
			for(;page_index<divList.length;page_index++){
				if(cmd<divList[page_index].offsetTop){
					break;
				}
			}
			var min_page = page_index - 2;
			if(min_page<1)min_page = 1;
			///min_page = 1;
			var max_page = page_index+2;
			if(max_page>gdoc._pdfInfo.numPages)max_page = gdoc._pdfInfo.numPages;
			
			var stay = new Set();
			var goaway = new Set();
			var newRender = new Set();
			
			for(var i = min_page;i<=max_page;i++){
				var oks = false;
				for(var j = 0;j<rendering.length;j++){
					if(i==rendering[j]){
						stay.add(i);
						oks = true;
						break;
					}
				}
				if(!oks){
					newRender.add(i);
				}
			}
			
			for(var j = 0;j<rendering.length;j++){
				var inrender = false;
				if(rendering[j]>=min_page && rendering[j]<=max_page){
					stay.add(rendering[j]);
				}else{
					goaway.add(rendering[j]);
				}
			}
			rendering.length = 0;
			for(var i = min_page;i<=max_page;i++)rendering.push(i);
			
			goaway.forEach((e1,e2,set)=>{
				console.log("drop page"+e1);
				console.log("canvas dropping:"+e1);
				gdoc.getPage(e1).then(page =>{
					page.cleanup();
				});
			});
			
			newRender.forEach((e1,e2,set)=>{
				console.log("canvas rendering:"+e1);
				rendering.push(e1);
				renderCanvas($container,gdoc,e1,zoomRatio);
			});
			
			
}
function renderCanvas2($container,doc,i,scale){
	doc.getPage(i).then(page =>{
		var div = divList[page.pageIndex];
		div.innerHTML = "";
		var pdfPageView = new pdfjsViewer.PDFPageView({
			container: div,
			id: i,
			scale: scale,
			defaultViewport: page.getViewport({ scale: scale, }),
      // We can enable text/annotations layers, if needed
			textLayerFactory: new pdfjsViewer.DefaultTextLayerFactory(),
			annotationLayerFactory: new pdfjsViewer.DefaultAnnotationLayerFactory(),
		});
    // Associates the actual page with the view, and drawing it
		pdfPageView.setPdfPage(page);
		return pdfPageView.draw();
	});
}
function renderCanvas($container,doc,i,scale){
	var zooming = 1.5;
	doc.getPage(i).then(page =>{
		var div = canvasList[page.pageIndex];
		div.innerHTML = "";
		
		var viewport = page.getViewport(scale*zooming);
		var canvas = document.createElement("canvas");
		var context = canvas.getContext("2d",{
			alpha: false
		});
		context.imageSmoothingEnabled = false;
		context.webkitImageSmoothingEnabled = false;
		context.mozImageSmoothingEnabled = false;
		canvas.height = viewport.height*zooming;
		canvas.width = viewport.width*zooming;
		canvas.style.height = viewport.height+"px";
		canvas.style.width = viewport.width+"px";
		canvas.mozOpaque = true;
		div.appendChild(canvas);
		//page.cleanup();
		page.render({
			canvasContext : context,
			viewport : viewport,
			enableWebGL: true
		});
	});
}

function renderDrawLayer(pageIndex){
	drawLayer = objList[pageIndex].drawLayer;
	drawLayer.innerHTML = "";
	tables = objList[pageIndex].tables;
	page = divList[pageIndex];
	currentHeight = page.offsetHeight;
	currentWidth = page.offsetWidth;
	for(var i =0;i<tables.length;i++){
		var table = tables[i];
		var ratioH = currentHeight/table.pageHeight;
		var ratioW = currentWidth/table.pageWidth;
		var innerBox = document.createElement("div");
		innerBox.setAttribute("class","inner-box");
		drawLayer.appendChild(innerBox);
		$(innerBox).css(
				'top', table.top*ratioH
			).css(
				'left', table.left*ratioW
			).css(
				'height', table.height*ratioH
			).css(
				'width', table.width*ratioW
			);
	}
}

function renderPDFText($container,doc,i,scale){
	return doc.getPage(i).then(page =>{
		//var scale = detectZoom();
		var viewport = page.getViewport(scale);
		var div = divList[page.pageIndex];
		div.innerHTML = "";
		div.setAttribute("id",'page-'+page.pageIndex);
		//div.setAttribute("style","position: relative");
		div.setAttribute("class","page");
		div.style.height = viewport.height+"px";
		div.style.width = viewport.width+"px";
		
		var canvasWrapper = document.createElement("div");
		canvasWrapper.style.height = viewport.height+"px";
		canvasWrapper.style.width = viewport.width+"px";
		canvasWrapper.setAttribute("class","canvasWrapper");
		div.appendChild(canvasWrapper);
		var loadingIcon = document.createElement("div");
		loadingIcon.setAttribute("class","loadingIcon");
		canvasWrapper.appendChild(loadingIcon);
		
		//haccumulate+= viewport.height;
		harray.push(div.offsetTop);
		
		var drawLayer = document.createElement("div");
		drawLayer.style.height = viewport.height+"px";
		drawLayer.style.width = viewport.width+"px";
		drawLayer.setAttribute("class","drawLayer");
		div.appendChild(drawLayer);

		
		var textLayer = document.createElement("div");
		textLayer.style.height = viewport.height+"px";
		textLayer.style.width = viewport.width+"px";
		textLayer.setAttribute("class","textLayer");
		div.appendChild(textLayer);
		
		var annotationWrapper = document.createElement("div");
		annotationWrapper.setAttribute("class","annotationLayer");
		div.appendChild(annotationWrapper);
		
		if(canvasList.length<=page.pageIndex)
		{
			canvasList.push(canvasWrapper);
			pageList.push(page);
			objList[page.pageIndex].canvas = canvasWrapper;
			objList[page.pageIndex].textLayer = textLayer;
			objList[page.pageIndex].annotationLayer = annotationWrapper;
			objList[page.pageIndex].drawLayer = drawLayer;
		}
		renderDrawLayer(page.pageIndex);
		//console.log(viewport.transform);
		var vp = viewport.transform;
		var t = viewport.clone({
			dontFlip: true
		});
		page.getAnnotations().then(annotation =>{
			var annotationParam = {
				annotations : annotation,
				viewport: t,
				div: annotationWrapper,
				page : page,
				linkService : simpleLinkService,
				downloadManager: null,
				renderInteractiveForm : false
			};
			pdfjsLib.AnnotationLayer.render(annotationParam);
		}).then(()=>{
			viewport.transform = vp;
		});
		
		return page.getTextContent().then(textContent =>{
			pdfjsLib.renderTextLayer({
				textContent: textContent,
				container: textLayer,
				viewport: viewport,
				enhanceTextSelection: true
			});
			return textLayer;
		});
		
	});
}


function getPageBase(idx){
	console.log(idx);
	console.log(harray[idx]);
	return harray[idx]+13*idx;
	//return idx*(pageHeight+13);
}


function getPageSingle(idx){
	return harray[idx+1]-harray[idx];
}