# web-alasql.md
https://dreamhack.io/wargame/challenges/941
## Description
nodejs alasql 패키지에 포함된 alaserver가 작동합니다.
플래그는 /flag 를 실행하면 얻을 수 있습니다.
해당 문제는 숙련된 웹해커를 위한 문제입니다.

# Exploit
docker-entrypoint.sh
```
#!/bin/bash
su node -s /bin/sh -c "while [ 1 ];do alaserver;done"
# while [ 1 ];do sleep 10000;done
```

alaserver이 작동되는 간단한 웹서비스이다.
`?<query>` 방식으로 쿼리를 날릴 수 있다.

alasql도 ejs와 비슷하게 익스플로잇 된다.

```
this.columns.forEach(function (col) {
	s += "r['" + col.column.columnid + "']=" + col.expression.toJS('r', '') + ';';
});
// console.log(423623, s);
var assignfn = new Function('r,params,alasql', 'var y;' + s);
```

만약 `col.column.columnid`의 값이 `0'+alert("UPDATE pwned")+'` 일 경우에 `s` 변수에 할당된 후 new function에 들어가고 쿼리가 실행된다.
