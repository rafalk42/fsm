var el = React.createElement;

var Binder = React.createClass({
	handleClick: function (id, event)
	{
		// event.preventDefault();
		this.props.onTabChange(id);
	},
	renderMenu: function ()
	{
		var self = this;
		var elements = this.props.children.map(
			   function (child, index)
			   {
				   return (el("li",
						 {
							 key: child.props.id,
							 className: "menu-item three columns"
						 },
				   el("a",
						 {
							 href: "#" + child.props.id,
							 onClick: self.handleClick.bind(self, child.props.id)
						 },
				   child.props.label)));
			   });
		return (
			   el(
					 "ul",
					 null,
					 elements)
			   );
	},
	renderTabs: function ()
	{
		var tab = this.props.children[0];
		for (i = 0; i < this.props.children.length; i++)
		{
			if (this.props.children[i].props.id === this.props.selectedTab)
			{
				tab = this.props.children[i];
			}
		}
		return (
			   el("div",
					 {
						 // className: "row"
					 },
					 el("h1", null, tab.props.label),
					 tab)
			   );
	},
	render: function ()
	{
		return (
			   el(
					 "div",
					 {
						 className: "binder"
					 },
			   el(
					 "div",
					 {
						 className: "menu row"
					 },
			   this.renderMenu()),
					 this.renderTabs())
			   );
	}
});
