def get_form_request_data(request):
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return email, password
    return None, None


def get_user_data(request, user_type, shop):
    shop_name = request.args.get('shop', type=str)
    if shop_name:
        shop_ = shop.query.filter_by(shop_name=shop_name).first()
        email, password = get_form_request_data(request)
        if email:
            try:
                user = user_type.query.filter_by(shop_id=shop_.id, email=email).first()
            except AttributeError as e:
                return False, email, password, None
            return True, email, password, user
    return False, None, None, None

