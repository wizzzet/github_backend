from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'

    menu = [
        ParentItem(
            'Страницы',
            children=[
                ChildItem(model='pages.homepage'),
                ChildItem(model='pages.flatpage'),
                ChildItem(model='pages.contactspage')
            ]
        ),
        ParentItem(
            'Брокеры',
            children=[
                ChildItem(model='brokers.brokerspage')
            ]
        ),
        ParentItem(
            'Реферральная программа',
            children=[
                ChildItem(model='referrals.referralprogrampage')
            ]
        ),
        ParentItem(
            'Услуги',
            children=[
                ChildItem(model='services.service'),
                ChildItem(model='services.servicespage')
            ]
        ),
        ParentItem(
            'Принятые формы',
            children=[
                ChildItem(model='forms.booking'),
                ChildItem(model='forms.partnershiprequest'),
                ChildItem(model='forms.brokerrequest')
            ]
        ),
        ParentItem(
            'SEO',
            children=[
                ChildItem(model='seo.redirect')
            ]
        ),
        ParentItem(
            'Основное',
            children=[
                ChildItem(model='core.gallery')
            ]
        ),
        ParentItem(
            'Настройки',
            children=[
                ChildItem(model='vars.menu'),
                ChildItem(model='vars.menuitem'),
                ChildItem(model='vars.siteconfig'),
                ChildItem(model='vars.bookingemailsettings'),
                ChildItem(model='vars.partneremailsettings')
            ]
        ),
        ParentItem(
            'Пользователи',
            children=[
                ChildItem(model='users.user'),
                ChildItem(model='auth.group')
            ]
        )
    ]
