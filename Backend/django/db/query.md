# query
데이터 models를 만들면 django에서 자동으로 여러 기능들이 구현된 api를 제공한다.

## 생성
```py
>>> p = Post(title="Hi", content="Hi")
>>> p.save()
```
sql의 INSERT문으로 변경된다. P가 호출될때까지 django는 db에 접근하지 않는다.

## 변경
```py
p.title = "Bye"
p.save()
```
sql의 UPDATE문으로 변경된다. p가 호출될때까지 db에 접근하지 않는다.

## 외래키 저장
```py
p = Post.objects.get(pk=1)
c = Comment.objects.get(pk=1)
c.post = p
c.save()

# n:n
c.post.add(a, b, c, d)
```
외래키에 객체를 할당해서 저장한다.

## 검색
객체를 검색할땐 QuertSets을 통해서 검색한다.      
QuerySets은 objects를 호출해서 얻는다.
```py
Post.objects.all()
```

## 필터
all()은 모든 객체들을 선택한다. 여기서 필터링을 하는건 2가지 방법이 있다.

### filter
쿼리셋에서 filter에 주어진 조건에 따라서 새로운 객체를 반환한다.

### exclude
조건에 일치하지 않는 새 객체를 반환한다.

```py
Product.objects.filter(title__startwith="hi")
Product.objects.all().filter(title__startwith="hi")
```
두 코드는 같은 역할을 한다.

```py
Product.objects.filter(title__startwith="hi")
.exclude(content__startwith="bye")
.filter(user=request.user)
```
이렇게 필터 체이닝도 할 수 있다.

## 단일 객체 검색
```py
Product.objects.get(id=1)
```
단 하나의 객체만 반환된다. 

## Limiting
```py
Post.obejcts.all()[:5]
```
첫번째 5개의 객체만 가져온다.

**[-1]** 방식의 인덱싱은 작동하지 않는다.
```py
Post.objects.all()[:10:2]
```
10개마다 각 2번째 객체가 리턴된다.

## 관계 검색
```py
Post.object.filter(blog__name="hello")
Post.object.filter(blog__name__contains="hello")
Post.object.filter(blog__authors__name__contains="Kim")
```
이런식으로 `__` 를 사용해서 확장시킬 수 있다.

## 캐싱
QuerySets의 접근을 최소화하기위해 캐싱이 된다.

## 동기/비동기
for문을 사용해서 쿼리를 조회할때 뒤에서 django가 자동으로 블로킹 하는 쿼리를 실행한다.    
그래서 비동기 뷰나 비동기 코드를 작성하면 orm을 사용 할 수 없다.

하지만 비동기쿼리 api를 사용하면 비동기 코드를 작성할 수 있다.    
`get(), delete()`는 `aget(), adelete()`등으로 사용 가능하다.

for문으로 쿼리를 사용하면 결과를 로드하는 중, django가 블록킹하는 쿼리를 실행한다.     
하지만 async for 을 사용하면 비동기적으로 호출할 수 있다.

```py
async for a in Authors.objects.filter(name__startswith="A"):
```
   
get(), first()같은 manage 쿼리는 강제로 실행되면서 db를 블로킹을 한다.    
하지만 쿼리셋에서 실행하는 경우(filter, exclude)는 db에 쿼리를 날리지 않기 때문에 비동기 코딩에 자유롭다.

```py
user = await User.objects.filter(username=my_input).afirst()
```
하지만 first()를 사용해야하는 경우에는 afirst()를 사용하는 방식처럼 비동기 친화적으로 코딩할 수 있다.

## Q
```py
from django.db.models import Q
```
Q는 더 복잡한 쿼리를 사용해야할때 사용된다.     
```py
Q(username__startswith="Kim")
```
`&, |, ^` 연산자를 사용할때 Q쿼리는 합쳐질 수 있다.
```py
Q(username__startswith="Kim") | Q(username__startswith="Jo")
# WHERE username LIKE 'Kim%' OR username LIKE 'Jo%'
```
`^`를 사용하려 하면 `~` 를 사용하며 부정한다.
```py
Q(username__startswith="Kim") | ~Q(username__startswith="Jo")
```