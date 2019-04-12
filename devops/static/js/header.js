if (typeof jQuery === "undefined") {
	throw new Error("Js requires jQuery");
};
(function(window, $) {
	/**
	 * 处理左边菜单栏的选中问题
	 */
	var header = {
		init : function() {
			this.removeActive();
			this.addActive();
		},
		removeActive : function() {
			$('.action-url').removeClass("active");
		},
		addActive : function() {
			$('.action-url').each(function() {
				if ($(this).prop('href') == window.location.href) {
					$(this).addClass("active");
				}
			});
		}

	};

	$(document).ready(function() {
		header.init();
	});

})(window, jQuery);