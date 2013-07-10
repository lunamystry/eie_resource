(function() {
  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  Ehlane.Users.Index = Backbone.View.extend({
    template: template('index'),
    initialize: function() {
      this.users = new Ehlane.Users();
      this.users.on('all', this.render, this);
      this.users.fetch();
    },
    render: function() {
      this.$el.html(this.template(this));
      var usersView = new Ehlane.Users.List({collection: this.users});
      var form = new Ehlane.Users.Form({collection: this.users});
      this.$(".users_list").append(usersView.render().$el);
      this.$(".users_form").append(form.render().$el);
      return this;
    },
    count: function() { return this.users.length; }
  });

  Ehlane.Index = Backbone.View.extend({
    template: template('index'),
    initialize: function() {
    },
  });

  Ehlane.Groups.Index = Backbone.View.extend({
    template: template('groups'),
    initialize: function() {
      this.groups = new Ehlane.Groups();
      this.groups.on('all', this.render, this);
      this.groups.fetch();
    },
    render: function() {
      this.$el.html(this.template(this));
      var groupsView = new Ehlane.Groups.List({collection: this.groups});
      var form = new Ehlane.Groups.Form({collection: this.groups});
      this.$(".groups_list").append(groupsView.render().$el);
      this.$(".groups_form").append(form.render().$el);
      return this;
    },
    count: function() { return this.groups.length; }
  });

  Ehlane.Login = Backbone.View.extend({
    template: template('login'),
    initialize: function() {
      this.users = new Ehlane.Users();
      this.users.on('all', this.render, this);
      this.users.fetch();
    },
    render: function() {
      this.$el.html(this.template(this));
      var usersView = new Ehlane.Login.Form({collection: this.users});
      this.$(".login_form").append(usersView.render().$el);
      return this;
    },
    count: function() { return this.users.length; }
  });

  Ehlane.Users.User = Backbone.View.extend({
    events: {
      "click button": "delete"
    },
    template: template('index-user'),
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    fullname: function() { return this.model.fullname(); },
    username: function() { return this.model.username(); },
    gender: function() { return this.model.gender(); },
    address: function() { return this.model.address(); },
    email: function() { return this.model.email(); },
    school: function() { return this.model.school(); },
    phone_no: function() { return this.model.phone_no(); },
    cellphone_no: function() { return this.model.cellphone_no(); },
    role_id: function() { return this.model.role_id(); },
    delete: function() {
      this.model.destroy({wait: true});
    }
  });

  Ehlane.Groups.Group = Backbone.View.extend({
    events: {
      "click button": "delete"
    },
    template: template('groups-group'),
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    name: function() { return this.model.name(); },
    members: function() { return this.model.members(); },
    delete: function() {
      this.model.destroy({wait: true});
    }
  });

  Ehlane.Users.List = Backbone.View.extend({
    render: function() {
      /* loop over all the models, appending a view of that model */
      this.collection.each(function(user) {
        var view = new Ehlane.Users.User({model: user});
        // console.log(user.attributes);
        this.$el.append(view.render().el);
      }, this)  /* bind it to the Users rather than each user */
        return this;
    }
  });

  Ehlane.Groups.List = Backbone.View.extend({
    render: function() {
      this.collection.each(function(group) {
        var view = new Ehlane.Groups.Group({model: group});
        this.$el.append(view.render().el);
      }, this)
        return this;
    }
  });

  Ehlane.Users.Form = Backbone.View.extend({
    tagName: "form",
    className: "form",
    template: template('user-form'),
    events: {
      "submit": "submit"
    },
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    submit: function(event) {
      event.preventDefault();
      var user = this.collection.create({
        'first_name': this.$('#first_name input').val(),
        'last_name': this.$('#last_name input').val(),
        'username': this.$('#username input').val(),
        'email': this.$('#email input').val(),
        'gender': this.$('#gender input').val(),
        'address': this.$('#address input').val(),
        'school': this.$('#school input').val(),
        'phone_no': this.$('#phone_no input').val(),
        'cellphone_no': this.$('#cellphone_no input').val(),
        'role_id': this.$('#role_id input').val(),
      },{
        wait: true,
        success: function(model, response) {
          alert("Success");
          console.log(model);
        },
        error: function(model, response) {
          errors = $.parseJSON(response.responseText);
          for (var field in model.attributes) {
            if (model.attributes.hasOwnProperty(field)) {
              this.$('#' + field + " input").val(model.attributes[field]);
              this.$('#' + field).removeClass('error');
            }
          }
          for (var field in errors) {
            if (errors.hasOwnProperty(field)) {
              this.$('#' + field).addClass('error');
              this.$('#' + field + " .help-inline").html(errors[field].join("<br/>"));
            }
          }
        }
      });
    }
  });

  Ehlane.Groups.Form = Backbone.View.extend({
    tagName: "form",
    className: "form",
    template: template('group-form'),
    events: {
      "submit": "submit"
    },
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    submit: function(event) {
      event.preventDefault();
      var group = this.collection.create({
        'name': this.$('#name input').val(),
        'members': this.$('#members input').val(),
      },{
        wait: true,
        success: function(model, response) {
          alert("Success");
          console.log(model);
        },
        error: function(model, response) {
          errors = $.parseJSON(response.responseText);
          for (var field in model.attributes) {
            if (model.attributes.hasOwnProperty(field)) {
              this.$('#' + field + " input").val(model.attributes[field]);
              this.$('#' + field).removeClass('error');
            }
          }
          for (var field in errors) {
            if (errors.hasOwnProperty(field)) {
              this.$('#' + field).addClass('error');
              this.$('#' + field + " .help-inline").html(errors[field].join("<br/>"));
            }
          }
        }
      });
    }
  });

  Ehlane.Login.Form = Backbone.View.extend({
    tagName: "form",
    className: "form",
    template: template('login-form'),
    events: {
      "submit": "submit"
    },
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    submit: function(event) {
      event.preventDefault();
      var session = new Ehlane.Session();
      session.save({
        'username': this.$('#username input').val(),
        'password': this.$('#password input').val(),
      },{
        success: function(session, response) {
          console.log(response);
          location.hash = "#index";
        },
        error: function(model, response) {
          errors = $.parseJSON(response.responseText);
          for (var field in model.attributes) {
            if (model.attributes.hasOwnProperty(field)) {
              this.$('#' + field + " input").val(model.attributes[field]);
              this.$('#' + field + " .help-inline").html("");
              this.$('#' + field).removeClass('error');
            }
          }
          for (var field in errors) {
            if (errors.hasOwnProperty(field)) {
              this.$('#' + field).addClass('error');
              this.$('#' + field + " .help-inline").html(errors[field]);
            }
          }
        }
      });
    }
  });
})()
