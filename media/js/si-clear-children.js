/*--------------------------------------------------------------------------------
 SI.ClearChildren v1.0

 Instructions for use:

 0. Include the following rules in your CSS (IE Win 5 requires `clear_children` to 
	be display: inline; you can use the * html hack--just be sure to hide from IE 
	Mac):

 	.clear_children,.cc_tallest { position: relative; }
	.cc_tallest:after { content: ''; }

 1. Layout your elements using absolute positioning relative to a container with a 
	class of `clear_children` which contains only the absolutely positioned 
	elements (no other inline elements).

 2. This causes the containing element to collapse.

 3. Decide which contained element will be the deepest on the most occasions and 
	assign a class of `cc_tallest`. This will cause the containing element to 
	expand to the height of this element.

 4. Include this file.

 ---------------------------------------------------------------------------------*/
if (!SI) { var SI = new Object(); };
SI.ClearChildren =
{
	control			: null,
	watchInterval	: 50,
	height			: 0,
	initialize		: function()
	{
		// IE Mac chokes on this (width and height assignments in particular). Go fish.
		if (document.createElement && !(document.all && !window.print))
		{
			var c = document.createElement('div'), s = c.style;
			s.position		= 'fixed';
			s.top			= '0';
			s.visibility	= 'hidden';
			s.width			= '1.em';
			s.height		= '1.em';
			this.control = document.body.appendChild(c);
			this.height = 0;
			window.setInterval('SI.ClearChildren.monitor()', this.watchInterval);
		};
		this.clear();
	},
	
	monitor	: function()
	{
		var o = this.height;
		this.height = this.control.offsetHeight;
		if (o != this.height) { this.clear(); };
	},
	
	clear : function()
	{
		if (!document.getElementsByTagName && !document.all) { return; }

		var elems = (document.all) ? document.all : document.getElementsByTagName('*');
		for (var i = elems.length-1; i >= 0; i--)
		{
			var elem = elems[i];
			if (!elem.className.match(/\bclear_children\b/)) { continue; };
			var container = elem;
			var tallest;
			var maxHeight = 0;
			for (var j = 0; j < container.childNodes.length; j++)
			{
				var contained = container.childNodes[j];
				if (contained.nodeType == 1)
				{
					if (contained.offsetHeight > maxHeight)
					{
						maxHeight	= contained.offsetHeight;
						tallest		= contained;
					};
					contained.className = contained.className.replace(/\bcc_tallest\b/, '');
				};
			};
			// Add to the front of the existing classes to appease IE Mac. Save me Jeebus. 
			tallest.className = 'cc_tallest' + ((tallest.className == '') ? '' : ' ' + tallest.className);
		};
	}
};

// Just do it.
SI.ClearChildren.initialize();