"""yasuo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny


doc_description = """
# API使用说明

api遵循rest设计规范

* GET：读取（Read）
* POST：新建（Create）
* PUT：更新（Update）
* PATCH：更新（Update），通常是部分更新
* DELETE：删除（Delete）

## Response返回结果规则

返回结果通过http状态码进行判别

### 2xx (`200` `201` `204`)

只要返回2xx的状态码都代表成功，返回内容里面没有特殊结构，例如(登陆成功)：

```json
{
    "token": "71af586177718ec7e6a81e83dff9bcas901fc07c"
}
```

### 400

代表失败，一般用于参数校验返回错误信息。解包后`detail`字段内为详细信息，例如(登陆时验证手机号及短信验证码)：

```json
{
    "msg": "Invalid Params",
    "detail": {
        "phone": [
            "The phone number is incorrect."
        ],
        "sms_code": [
            "The verification code is incorrect or has expired"
        ]
    }
}
```

### 401

未认证(token校验未通过)

### 404

请求的资源未找到

### 403

权限不足

## Token认证

登陆用户会为其创建token，除个别api外(发短信、登陆。。等等)，默认都会进行Token认证。请求api时需添如下类似header，后面那段字符替换未用户自己的Token

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```
"""


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('docs/', include_docs_urls(title='Documents', description=doc_description, permission_classes=(AllowAny, ))),
]
