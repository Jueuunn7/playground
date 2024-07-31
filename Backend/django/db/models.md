# models
모델은 하나의 정보데이터이다. 일반적으로 각 모델은 db 테이블에 매칭된다.

1. 모델은 db 테이블에 매핑된다.
2. 모델의 속성은 테이블의 각 필드를 나타낸다.
3. 이 모델을 통해서 orm이 작동한다.

# 예시
```py
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
```

**username**과 **password**는 모델의 필드이다. 각 필드는 클래스의 어트리뷰트이다.

테이블을 생성하는 sql문은 이렇다
```sql
CREATE TABLE ${appname}_User (
    "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "username" varchar(30) NOT NULL,
    "password" varchar(255) NOT NULL
);
```
- 테이블 이름은 **${app_name}_\${model_name}**으로 작성된다.
- id는 자동으로 생성되지먄 직접 정의할 수 있다.
- 연결된 db에 따라서 sql문은 다르게 생성된다.

# 필드
```py
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=255)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    zipcode = models.CharField(max_length=6)
```

## 필드 옵션
필드에 들어갈 수 있는 옵션들이다. 특정 필드별로 필요한 옵션이 있다.     
**CharField**는 **max_length**가 필요함 등등

### null
null값 허용 여부이다. default는 False
### blank
필드를 비우는게 허용되는지 여부이다 default는 False.
null과의 차이점은 null은 db와 관련이 있지만 blank는 form에서 빈 값 허용 여부이다.
### choices
```py
COUNTRY = [
    ("KO", "Korea"),
]

country = models.CharField(choices=COUNTRY, max_length=2)
```
db엔 KO로 저장되고 Korea로 매핑된다.
### default
필드의 기본값을 지정해준다.
### help_text
form에서 사용되는 도움말이다.
### primary_key
기본키 여부를 결정한다.
**primary_key=True**가 없으면 자동으로 django에서 생성해준다.
### unique
unique는 테이블에서 고유한 값을 지정하는데 사용된다.

# 관계
### n:1
다대일 관계에서는 **ForeignKey**를 사용한다.
```py
class User(models.Model):
    pass

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```

### n:n
다대다 관계에서는 **ManyToManyField**를 사용한다.
```py
class User(models.Model):
    pass

class Phone(models.Model):
    user = models.ManyToManyField(User)
```

##### 1:1
일대일 관계에서는 **OneToOneField**를 사용한다.
```py
class User(models.Model):
    pass

class Phone(models.Model):
    user = models.OneToOneField(User)
```

## Meta
**class Meta**를 사용해서 테이블의 메타데이터를 설정할 수 있다.

### app_label 
앱 외부에서 모델이 정의되면 앱을 직접 지정할 수 있다.

### db_table 
테이블 이름을 직접 지정할 수 있다.

### unique_together
두 개의 필드를 같이 묶어 유니크하게 만들 수 있다.
**unique_together = [["driver", "restaurant"]]**