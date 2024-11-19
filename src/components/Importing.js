import { SERVER_INFO} from './config.js';

// 데이터를 저장할 객체 초기화
const importedData = {}; 

// fetchData 함수 정의 및 내보내기
export async function fetchData(resource) {
    const url = `http://${SERVER_INFO.host}:${SERVER_INFO.port}${SERVER_INFO.basePath}/${resource}/la`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'X-M2M-Origin': 'CAdmin', 
                'X-M2M-RVI': '3',         
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch ${resource}: ${response.status}`)
        }

        const data = await response.json()
        console.log("받아온데이터 (원본) ", data)

        const jsonString = JSON.stringify(data)
        console.log("파싱된 데이터:", jsonString)

        // 문자열화된 데이터에서 JSON으로 다시 파싱
        const parsedData = JSON.parse(jsonString)

        // 안전하게 'con' 값 추출
        let conValue = 'No data';
        if (parsedData && parsedData['m2m:cin'] && parsedData['m2m:cin'].con){
            conValue = parsedData['m2m:cin'].con
        }
        console.log(resource + '의 con 값:', conValue)
        return conValue

    } catch (error) {
        console.error(`Error fetching ${resource}:`, error)
        return null 
    }
}
