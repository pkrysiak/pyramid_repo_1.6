
<%inherit file="base.mako"/>

<%block name = "content">
    <div class="main_box_left">
        <div class="name_product">
            Product name: ${product_name}
            % if allegro_link is None and nokaut_link is None:
                <p id="upper_space"> No such item... </p>
            %else:
                <p id="upper_space"> Links:</p>
                <p id="upper_space"><a href = "${allegro_link or '#'}" style="text-decoration: none"> ${allegro_link or 'No such item in allegro..'} </a></p>
                <p id="upper_space"><a href = "${nokaut_link or '#'}" style="text-decoration: none"> ${nokaut_link or 'No such item in nokaut..'} </a></p>
            % endif
        </div>
        <div class="box_photo">
            <p style="margin-top:250px"> <br></p>
       <!--     <img src="${request.static_url('pyramid_app:static/img/img_demo.jpg')}" alt="img_demo"/>-->
        </div>
    </div>
    <div class="main_box_right">
        <div class="compare_box">
            <img src="${request.static_url('pyramid_app:static/img/logo_allegro.png')}" alt="logo_allegro"/>
            <div class="price ${'win' if won == 'allegro' else ''}">${allegro_price or ''}</div>
        </div>
        <div class="compare_box">
            <img src="${request.static_url('pyramid_app:static/img/logo_nokaut.png')}" alt="logo_nokaut"/>
            <div class="price ${'win' if won == 'nokaut' else ''}">${nokaut_price or ''}</div>
        </div>
    </div>
</%block>