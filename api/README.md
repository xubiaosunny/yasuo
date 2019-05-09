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

## Signature认证

为防止api被人滥用，部分接口(如发短信)会进行Signature认证，请求需Signature认证的接口时需添如下类似header

```
Authorization: Signature 337f3fbccf03bada424fbb78b13107df 2019-05-08T10:26:00
```

认证内容分为三部分(认证方式 签名 日期)，中间使用空格隔开

日期使用UTC时间，格式方式为`yyyy-MM-dd'T'HH:mm:ss`

生成签名的方式：取 `ACCESS_KEY`+URI+时间字符串 的MD5

如下为生成签名的java示例代码

```java
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.text.SimpleDateFormat;
 

public class SignatureHelper {
    private static final String ACCESS_KEY = "f$)+n6&a0)t2x6ccz!5ko1%rtsry1)9_xug2e+1#er%r)6g*)w";
    public static String getSignature() {
        String time = getDate();
        String url = "/api/auth/send_sms_code/";
        try {
            MessageDigest digest = MessageDigest.getInstance("MD5");
            digest.update(ACCESS_KEY.getBytes());
            digest.update(url.getBytes());
            digest.update(time.getBytes());
            return getHashString(digest);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        return null;
    }

    public static String getDate() {
        final java.util.Calendar cal = java.util.Calendar.getInstance(); 
		// System.out.println(cal.getTime());
		//2、取得时间偏移量：  
		final int zoneOffset = cal.get(java.util.Calendar.ZONE_OFFSET); 
		// System.out.println(zoneOffset);
		//3、取得夏令时差：  
		final int dstOffset = cal.get(java.util.Calendar.DST_OFFSET);  
		// System.out.println(dstOffset);
		//4、从本地时间里扣除这些差量，即可以取得UTC时间：  
        cal.add(java.util.Calendar.MILLISECOND, -(zoneOffset + dstOffset)); 
        // System.err.println(cal.getTime());
        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
        String time = format.format(cal.getTime());
        System.err.println(time);
        return time;
    }
 
    private static String getHashString(MessageDigest digest) {
        StringBuilder builder = new StringBuilder();
        for (byte b : digest.digest()) {
            builder.append(Integer.toHexString((b >> 4) & 0xf));
            builder.append(Integer.toHexString(b & 0xf));
        }
        return builder.toString();
    }
    public static void main (String[] args) {
        String s = getSignature();
        System.out.println(s);

    }
}
```