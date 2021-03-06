
def index():
    return dict()
def movie():
    return dict()
    
@auth.requires_login()
def add_review():
    return dict()

@auth.requires_login()
def my_review():
    return dict()

@auth.requires_login()
def my_liked_review():
    return dict()

@auth.requires_login()
def view_profile():
    profile = db.profile(request.args(0))
    
    user_email = request.vars.email or auth.user.email

    pro = db(db.profile.email == user_email).select().first()

    if pro is None:
         redirect(URL('default', 'edit_profile'))
    
    else:
        
        form = SQLFORM(db.profile, pro, readonly = True)
           
    
    return dict(form=form)

@auth.requires_login()
def edit_profile():
    profile = db.profile(request.args(0))
    
    user_email = request.vars.email or auth.user.email

    pro = db(db.profile.email == user_email).select().first()

        
    if pro is None: 
        form = SQLFORM(db.profile,  pro)
        if form.process().accepted: # process form after either if statement executes
            
            redirect(request.vars.next or URL('default', 'view_profile'))
        
        # edit
        # not updating properly

    profile = db.profile(request.user_email)

    if pro is not None: 
            
        form = SQLFORM(db.profile, pro) 
        if form.process().accepted:
            redirect(request.vars.next or URL('default', 'view_profile'))

    return dict(form=form)



# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

@auth.requires_login()
def api_get_user_name():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'name':auth.user.first_name + '' +
        auth.user.last_name})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
