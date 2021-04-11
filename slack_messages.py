import rst


def generate_new_reservation_slack_message(data):
    tpl = rst.env.get_template('new_reservation_fr.txt')
    txt = tpl.render(data)
    return txt