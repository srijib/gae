$(function() {
	var $document = $(document);
	var $window = $(window);
	var $content = $('#content');
	var $loading = $('<div/>');
	var loading = false;
	var $next_url = $('#content>.post-nav>.previous>a');
	var complete = false;
	var next_url = '';

	function set_next_url() {
		if ($next_url.length) {
			complete = false;
			next_url = $next_url.attr('href');
		} else {
			complete = true;
			next_url = '';
		}
	}
	set_next_url();

	function load() {
		$loading.load(next_url + ' #content', function() {
			$next_url = $loading.find('.post-nav>.previous>a');
			set_next_url();
			$('#content>.post-nav').remove();
			$loading.children().remove().children().hide().appendTo($content).slideDown(1000);
			loading = false;
		});
		_gaq.push(['_trackEvent', 'Page', 'Load', next_url]);
	}

	$window.scroll(function(){
		if (!complete && !loading && ($document.height() - $window.scrollTop() - $window.height() < 100)) {
			loading = true;
			load();
		}
	});
});