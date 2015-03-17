//
// comment-view.js
// ===============

// Widok pojedynczego komentarza.

define(['jquery',
		'underscore',
		'backbone',
		'js/modules/comments/comment-model',
		'js/modules/comments/subcomment-collection'],

function ($, _, Backbone, CommentModel, SubcommentCollection) {
	
"use strict";

var currentLang = CivilApp.language;

var CommentView = Backbone.View.extend({
	
	tagName: 'div',
	
	className: 'comment',
	
	template: _.template($('#comment-template').html()),
	
	initialize: function () {
		var url = '/rest/comments/' + this.model.get('id') + '/replies/';
		$.get(url, function (resp) {
			this.collection = new SubcommentCollection(resp);
			this.renderReplies();
		}.bind(this));
	},
	
	render: function () {
		//dodaje tooltip dla glosowania pod kazdym komentarzem
		$('.comment-meta-options').find('a').tooltip();
		
		// Wyświetlenie bieżącego komentarza
		this.$el.html(this.template(this.model.toJSON()));
		
		// Głosowanie ZA
		this.$el.find('.vote-up-link').click(function (e) {
			e.preventDefault();
			this.voteUp();
		}.bind(this));
		
		// Głosowanie PRZECIW
		this.$el.find('.vote-down-link').click(function (e) {
			e.preventDefault();
			this.voteDown();
		}.bind(this));
		
		// Odpowiedz na komentarz
		this.$el.find('.comment-reply').on('click', function (e) {
			e.preventDefault();
			this.replyComment();
		}.bind(this));
		
		// Pokaż/ukryj odpowiedzi do tego komentarza
		this.$el.find('.show-replies').on('click', function (e) {
			e.preventDefault();
			if (this.collection.length) {
				this.toggleReplies();
			} else {
				return false;
			}
		}.bind(this));
		
		// Pokaż/ukryj kontrolki
		this.$ctrls = this.$el.find('.comment-controls:first');
		this.$el.on('mouseover', function (e) {
			e.stopPropagation();
			this.$ctrls.animate({opacity:1}, {
				duration: 'fast',
				queue: false,
				stop: true
			});
		}.bind(this));
		this.$el.on('mouseout', function (e) {
			e.stopPropagation();
			this.$ctrls.animate({opacity:0}, {
				duration: 'fast',
				queue: false,
				stop: true
			});
		}.bind(this));
		
		// Edycja istniejącego komentarza
		if (this.$ctrls.find('.comment-edit').length > 0) {
			this.$ctrls.find('.comment-edit').on('click', function (e) {
				e.preventDefault();
				this.editComment();
			}.bind(this));
		}
			
		return this;
	},
	
	editComment: function () {
		// Nie otwieramy edycji, jeżeli już jest uruchomiona!
		if (this.nowEdited !== undefined) return false;
		
		// Edytujemy istniejący komentarz. Templatka dla edycji i dodawania
		// jest inna!!!
		var $ed = $(_.template($('#comment-edit-template').html(), {}));
		var txt = this.model.get('comment');
		
		// Zaznaczamy komentarz jako aktualnie edytowany, żeby otwierać tylko
		// jedno okienko edycji
		this.nowEdited = true;
		
		// Zastępujemy komentarz edytorem.
		this.$el.find('.comment-content:first').empty().append($ed);
		// Uzupełniamy edytor starym komentarzem.
		$ed.find('#comment').val(this.model.get('comment'));
		
		// Zapisz nową wersję komentarza
		$ed.find('.btn-submit-comment').on('click', function (e) {
			e.preventDefault();
			this.model.url = '/rest/comments/' + this.model.get('id') + '/';
			this.model.save({
				comment: $ed.find('#comment').val(),
				submit_date: moment().format()
			}, {patch: true}); // update przez PATCH
			// Usuń edytor i pokaż zaktualizowany komentarz.
			$ed.empty().remove();
			delete this.nowEdited;
			this.$el.find('.comment-content:first')
				.text(this.model.get('comment'));
		}.bind(this));
		
		// Anulowanie akcji - przerwanie edycji
		$ed.find('.btn-cancel-comment').on('click', function (e) {
			e.preventDefault();
			$ed.empty().remove();
			delete this.nowEdited;
			this.$el.find('.comment-content:first').text(txt);
		}.bind(this));
	},
	
	renderReplies: function () {
		// Wyświetla listę odpowiedzi tworząc widoki dla każdej odpowiedzi
		// w kolekcji.
		this.collection.each(function (item) {
			// Określamy listę, żeby nie dodawać odpowiedzi do odpowiedzi:
			var $list = this.$el.find('.subcomments:first');
			var comment = new CommentView({model:item});
			comment.parentView = this.parentView;
			// Dodajemy komentarze do przygotowanej listy
			$(comment.render().el).appendTo($list);
		}, this);
	},
	
	replyComment: function () {
		// Jak przy edycji upewniamy się że tylko jedno okienko jest otwarte
		if (this.parentView.nowAnswered !== undefined) {
			if (this.parentView.nowAnswered === this) return false;
			this.parentView.nowAnswered.$el.
				find('form, .comment-avatar-col').empty().remove();
		}
		// Oznaczamy komentarz jako "otwarty" do odpowiedzi.
		this.parentView.nowAnswered = this;
		
		// Odpowiedz na komentarz. Ta funkcja z pewnością może wyglądać lepiej.
		var $form = $(_.template($('#comment-form-template').html(), {}));
		// Musimy się upewnić, że dodajemy elementy do parenta, a nie któ-
		// rejś z odpowiedzi.
		var $list = $(this.$el.find('.subcomments:first'));
		// Pokaż formularz po naciśnięciu odnośnika
		$form.insertBefore($list);
		// Submit formy - tworzymy faktyczny komentarz
		$form.on('submit', function (e) {
			e.preventDefault();
			var model = new CommentModel({
				comment: $form.find('textarea').val(),
				parent: this.model.get('id')
			});
			// Nie dopuszczamy pustych komentarzy
			if (model.get('comment').length <= 0) {
				alert(gettext("Comment cannot be empty"));
				return false;
			}
			// FIXME: model url przypisujemy ręcznie ze względu na problemy
			// z kontrolowanie eventów na wewnętrznych elementach. Warto po-
			// szukać lepszego rozwiązania i oddelegować te zadania kolekcji.
			model.url = '/rest/comments/';
			var comment = new CommentView({
				model: model
			});
			this.collection.add(model);
			model.save();
			$form.empty().remove();
			// Kolejny paskudny element - to powinno być wywołane po dodaniu
			// nowego elementu do kolekcji.
			$(comment.render().el).appendTo($list);
			delete this.parentView.nowAnswered;
		}.bind(this));
		// Anulowanie czynności - zamykamy okienko edycji
		$form.find('.btn-cancel-comment').on('click', function (e) {
			e.preventDefault();
			$form.empty().remove();
			delete this.parentView.nowAnswered;
		}.bind(this));
	},
	
	toggleReplies: function () {
		// Pokaż/ukryj odpowiedzi do tego komentarza.
		var $toggle = this.$el.find('.show-replies'),
			$sublist = this.$el.find('.subcomments');

		if ($sublist.is(':visible')) {
			$sublist.slideUp('fast', function () {
				$toggle.text(gettext('(show)'));
			});
		} else {
			$sublist.slideDown('fast', function () {
				$toggle.text(gettext('(hide)'));
			});
		}
	},
	
	_sendVote: function (vote, vStart) {
		var self = this,
			vTotal = this.model.get('total_votes'),
			totalVotes = vote == 'up' ? ++vTotal : --vTotal,
			votes = ++vStart;

		$.ajax({
			type: 'POST',
			url: '/rest/votes/',
			data: {
				vote: vote,
				comment: self.model.get('id')
			},
			// Response zwraca error wyłącznie w przypadku błędu serwera,
			// także w obiekcie `resp` przesyłamy dodatkowo informację
			// `success` (true lub false) i wyświetlamy odpowiedni alert.
			success: function (resp) {
				if (resp.success === true) {
					self.model.set('upvotes', votes);
					self.model.set('total_votes', totalVotes);
					// FIXME: przenieść to do jednej funkcji.
					self.render();
					self.renderReplies();
					message.success(resp.message);
				} else {
					message.alert(resp.message);
				}
			},
			error: function (err) {
				console.log(err);
			}
		});
	},
	
	voteUp: function () {
		this._sendVote('up', this.model.get('upvotes'));
	},
	
	voteDown: function () {
		this._sendVote('down', this.model.get('downvotes'));
	}
});

return CommentView;

});