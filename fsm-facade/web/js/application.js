var el = React.createElement;

var Application = React.createClass({
	getInitialState: function ()
	{
		var href = location.href.split("#");
		selectedTab = 0;
		if (href.length === 2)
		{
			selectedTab = href[1];
		}
		return {
			selectedTab: selectedTab
		};
	},
	handleTabChange: function (tabIndex)
	{
		this.setState({
			selectedTab: tabIndex
		});
	},
	render: function ()
	{
		return (
			el("div",
				null,
				el(Binder,
				{
					selectedTab: this.state.selectedTab,
					onTabChange: this.handleTabChange
				},
				el(ServerStatus,
				{
					id: "status",
					label: "Server status",
				}, null),
				el(ServerControl,
				{
					id: "control",
					label: "Server control",
				}, null)
				)
			)
		);
	}
});