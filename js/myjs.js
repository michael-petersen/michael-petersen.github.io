function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
} 

   $(document).scroll(function(){

	var body = document.body,
	    html = document.documentElement;

       var height = html.clientHeight - 50;
       var rmin = 11;
       var gmin = 29;
       var bmin = 63;
        t = (height - $(this).scrollTop())/height;
	t = Math.min(Math.max(0.,t),1.);
	r = Math.floor(t * (255-rmin))+rmin;
	g = Math.floor(t * (255-gmin))+gmin;
	b = Math.floor(t * (255-bmin))+bmin;
        if(t<0) t=0;
        document.getElementById('header').style.backgroundColor=rgbToHex(r,g,b);
	var aaa = document.getElementById('header')
	var bb = aaa.getElementsByTagName("h2");
       var cc = Math.floor((1.-t) * (255-51)) + 51;
       it = 1.-t;
       	r = Math.floor(it * (255-rmin))+rmin;
	g = Math.floor(it * (255-gmin))+gmin;
	b = Math.floor(it * (255-bmin))+bmin;
	for (var i = 0; i < bb.length; i++) {
	    bb[i].style.color = rgbToHex(r,g,b);
	}

	bb = aaa.getElementsByTagName("span");
        it = 1. - t;
	r = Math.floor(it * (255-rmin))+rmin;
	g = Math.floor(it * (255-gmin))+gmin;
	b = Math.floor(it * (255-bmin))+bmin;
	for (var i = 0; i < bb.length; i++) {
		bb[i].style.color = rgbToHex(r,g,b);
	}
       
       	bb = aaa.getElementsByTagName("li");
        it = 1. - t;
	r = 0//Math.floor(it * (26))-26;
	g = 0//Math.floor(it * (83))-83;
	b = 0//Math.floor(it * (255))-255;
	for (var i = 0; i < bb.length; i++) {
		bb[i].style.color = rgbToHex(r,g,b);
	}

    })
