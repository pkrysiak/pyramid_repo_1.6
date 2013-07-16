
<%inherit file="base.mako"/>

<%block name="login_form">
    <div class="form_login">
            <div class="head_login">Login in</div>
            % if errors:
                %for error in errors:
                    <p id="red"> ${error} </p>
                %endfor
            % endif
            <form method="post" action="/login">
                <input class="input_text" type="text" name="login" value="login"/>
                <input class="input_text" type="password" name="password" value="password"/>
                <button class="btn btn-primary" type=submit>Login</button>
            </form>
    </div>
</%block>