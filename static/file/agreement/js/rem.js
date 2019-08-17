(function (doc, win) {
	
	var docEl = doc.documentElement,
	    resizeEvt = 'orientationchange' in window ? 'orientationchange' : 'resize',
	    recalc = function () {
	      var clientWidth = docEl.clientWidth;
	      if (!clientWidth) return;
	      doc.getElementsByTagName("html")[0].style.fontSize = 100 * (clientWidth / 375) + 'px';
	    };
	    recalc();
		if (!doc.addEventListener) return;
		win.addEventListener(resizeEvt, recalc, false);
		doc.addEventListener('DOMContentLoaded', recalc, false);
})(document, window);















