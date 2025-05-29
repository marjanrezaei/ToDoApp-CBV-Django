{% extends "mail_templated/base.tpl" %}

{% block subject %}
Reset Your Password
{% endblock %}

{% block html %}
<a href="http://127.0.0.1:8000/accounts/api/v1/reset-password/confirm/{{token}}"> reset link </a>
{% endblock %}