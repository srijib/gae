(function(){
	var $scroller = null;
	var $body = $('body');
	var $html = $('html');
	if ($body.scrollTop()) {
		$scroller = $body;
	} else if ($html.scrollTop()) {
		$scroller = $html;
	} else {
		$body.scrollTop(1);
		if ($body.scrollTop()) {
			$scroller = $body.scrollTop(0);
		} else {
			$scroller = $html;
		}
	}
	function scrollTo(top) {
		$scroller.animate({scrollTop: top < 0 ? 0 : top}, 1000);
	}
	$('a[href^=#]').live('click', function(ev){
		var href = $(this).attr('href');
		if (href == '#') {
			scrollTo(0);
			ev.preventDefault();
		}
		var $href = $(href);
		if ($href.length) {
			scrollTo($href.offset().top);
			ev.preventDefault();
		}
	});
})();