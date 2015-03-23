//
// location-form.js
// ================

// Scripts to handle location form.

define(['jquery',
				'underscore',
				'backbone',
				'file-input',
				'js/modules/ui/mapinput'],

function ($, _, Backbone) {
	
"use strict";

// Base sublocations API url

var baseUrl = '/api-locations/sublocations/';

// Default text for trigger button

var defaultOpt = gettext("Click to select from list");

// Template for entire "syntetic" input group.

var inputTemplate = $('#input-tpl').html();

// Template for single option in 'select' element.

var optionTemplate = '<li class="name-entry" data-value="<%= id %>"><%= name %></li>';

// Template for faked element that replaces original select

var textTemplate = '<input type="text" name="parent" id="id_parent" value=\
					"<%= value %>" style="display:none;" />';

// Display currently selected place's name.

var $indicator = $('<input type="text" />');
$indicator.attr('readonly', 'readonly')
	.addClass('form-control indicator');

// Single "fake" input element
// ---------------------------

var InputElement = Backbone.View.extend({
	
	className: 'fake-input',
	
	template: _.template(inputTemplate),
	
	events: {
		'click .name-entry': 'expand',
		'click .input-indicator': 'toggleList',
		'keyup .search-filter': 'filter'
	},
	
	initialize: function (data) {
		this.parent = data.parent || undefined;
		this.parentId = data.parentId || null;
		// Sublocations fetched from server
		this.options = data.options || [];
	},
	
	renderOption: function (option) {
		var tpl = _.template(optionTemplate);
		this.$el.find('ul').append($(tpl(option)));
	},
	
	render: function () {
		if (this.options.length <= 0) {
			return false;
		}
		this.$el.html(this.template, null);
		_.each(this.options, function (option) {
			this.renderOption(option);
		}, this);
		this.select(defaultOpt);
		return this;
	},
	
	expand: function (e) {
		var id = $(e.currentTarget).attr('data-value'),
			name = $(e.currentTarget).text();
		
		if (this.parent !== undefined) {
			this.$el.nextAll('.fake-input')
				.empty().remove();
			this.parent.expand(id);
			$indicator.val(name);
			this.$el.find('.selected').removeClass('selected');
			$(e.currentTarget).addClass('selected');
			this.select(name);
			this.toggleList();
		}
	},
	
	// Show/hide sublocations list
	
	toggleList: function () {
		var $ul = this.$el.find('ul');
		$('ul.expanded').not($ul)
			.hide()
			.removeClass('expanded');
		this.$el.find('ul').toggle()
			.toggleClass('expanded');
		this.$el.find('.search-filter')
			.val('').focus();
		this.filter();
	},
	
	// Mark selected location and display it's name.
	//
	// @param name { string } Nazwa lokalizacji
	
	select: function (name) {
		var $i = this.$el.find('.input-indicator');
		$i.text(name);
		if (name !== defaultOpt) {
			$i.removeClass('btn-success')
				.addClass('btn-primary');
		}
	},
	
	// Fiter sublocations list
	
	filter: function () {
		var name = this.$el.find('.search-filter').val(),
			re = new RegExp(name, 'i');
		this.$el.find('.name-entry').each(function (item) {
			if (re.test($(this).text())) {
				$(this).show();
			} else {
				$(this).hide();
			}
		});
	}
});

// Location form
// -------------

var LocationForm = Backbone.View.extend({
	
	el:  "#new-location-form",
	
	initialize: function () {
		
		var parent = this;
		
		this.$el.find('[type="file"]')
			.bootstrapFileInput();

		// Minimap

		this.$el.find('#id_latitude')
			.before('<div id="map"></div>');
		this.$el.find('#id_latitude, #id_longitude')
			.css('display', 'none');
		this.$el.find('#map').mapinput({
			single: true,
			width : 664,
			height: 480,
			markers: CivilApp.markers,
			iconPath: ([CivilApp.staticURL, 'css', 'images']).join('/'),
			onchange: function (e, markers) {
				$('#id_latitude').val(e.lat);
				$('#id_longitude').val(e.lng);
			}
		});
		
		var value = $('#id_parent').val();
		
		// First 'faked' select input
		
		this.$fakeInput = new InputElement({
			parent: parent,
			options: CivilApp.countryList
		});
		
		// Keep real field value
		
		this.$realInput = $(_.template(textTemplate, {
			value: value
		}));
		
		$('#id_parent').replaceWith(this.$realInput);
		this.$indicator = $indicator;
		this.$indicator.insertAfter(this.$realInput);
		$(this.$fakeInput.render().el)
			.insertAfter(this.$realInput);

		// Fill parent name if we editing already existin location

		var parentId = parseInt($('#id_parent').val(), 10);
		if (!isNaN(parentId)) {
			$.get(('/api-locations/locations/{id}/').replace(/{id}/g, parentId),
				function (location) {
					$indicator.val(location.name);
				}
			);
		}
	},
	
	// Create another 'faked' input
	//
	// @param id { int } - ID of location, from which we want 'children'
	
	expand: function (id) {
		
		var url = ([baseUrl, '?pk=', id]).join(''),
			fake = null,
			parent = this;
		
		$.get(url, function (response) {
			if (response.length <= 0) {
				return false;
			}
			fake = new InputElement({
				parent: parent,
				parentId: id,
				options: response
			});
			$(fake.render().el)
				.insertAfter(this.$el.find('.fake-input').last());
		}.bind(this));
		
		this.$realInput.val(id);
	}
});

return LocationForm;

});
