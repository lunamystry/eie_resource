(function() {
  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  Resource.Users.Index = Backbone.View.extend({
    template: template('index'),
    initialize: function() {
      this.users = new Resource.Users();
      this.users.on('all', this.render, this);
      this.users.fetch();
    },
    render: function() {
      this.$el.html(this.template(this));
      var usersView = new Resource.Users.List({collection: this.users});
      var form = new Resource.Users.Form({collection: this.users});
      this.$(".users_list").append(usersView.render().$el);
      this.$(".users_form").append(form.render().$el);
      return this;
    },
    count: function() { return this.users.length; }
  });

  Resource.Index = Backbone.View.extend({
    template: template('index'),
    initialize: function() {
    },
  });

  Resource.Groups.Index = Backbone.View.extend({
    template: template('groups'),
    initialize: function() {
      this.groups = new Resource.Groups();
      this.groups.on('all', this.render, this);
      this.groups.fetch();
    },
    render: function() {
      this.$el.html(this.template(this));
      var groupsView = new Resource.Groups.List({collection: this.groups});
      var form = new Resource.Groups.Form({collection: this.groups});
      this.$(".groups_list").append(groupsView.render().$el);
      this.$(".groups_form").append(form.render().$el);
      return this;
    },
    count: function() { return this.groups.length; }
  });

  Resource.Login = Backbone.View.extend({
    template: template('login'),
    initialize: function() {
      this.users = new Resource.Users();
      this.users.on('all', this.render, this);
      this.users.fetch();
    },
    render: function() {
      this.$el.html(this.template(this));
      var usersView = new Resource.Login.Form({collection: this.users});
      this.$(".login_form").append(usersView.render().$el);
      return this;
    },
    count: function() { return this.users.length; }
  });

  Resource.Users.User = Backbone.View.extend({
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

  Resource.Groups.Group = Backbone.View.extend({
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

  Resource.Users.List = Backbone.View.extend({
    render: function() {
      /* loop over all the models, appending a view of that model */
      this.collection.each(function(user) {
        var view = new Resource.Users.User({model: user});
        // console.log(user.attributes);
        this.$el.append(view.render().el);
      }, this)  /* bind it to the Users rather than each user */
        return this;
    }
  });

  Resource.Groups.List = Backbone.View.extend({
    render: function() {
      this.collection.each(function(group) {
        var view = new Resource.Groups.Group({model: group});
        this.$el.append(view.render().el);
      }, this)
        return this;
    }
  });

  Resource.Users.Form = Backbone.View.extend({
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

  Resource.Groups.Form = Backbone.View.extend({
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

  Resource.Login.Form = Backbone.View.extend({
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
      var session = new Resource.Session();
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
