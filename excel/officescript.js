async function main(workbook: ExcelScript.Workbook) {
    const sheet = workbook.getWorksheet("Sheet1");
    var messages : IMessage[] =  [{
        role: "user", content: sheet.getRange("c2").getValue().toString()
    }];
    const payload: IPrompt = {
        messages,
        max_tokens: 100,
        temperature: 0.3
    };
    const settings = {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            'api-key':'<API_KEY>'
        },
        body: JSON.stringify(payload)
    };
    const crmGPTURI = 'https://<NAME>.openai.azure.com/openai/deployments/<DEPLOYMENT_NAME>/chat/completions?api-version=2023-07-01-preview';
    const fetchResult = await fetch(crmGPTURI, settings);
    const json: IChatCompletion = await fetchResult.json();
    sheet.getRange("c4").setValue(json.choices[0].message.content);
}
// GPT Interfaces
interface IPrompt { messages: IMessage[], max_tokens: number, temperature: number }
interface IMessage {role:string, content:string}
interface IUsage {prompt_tokens: number, completion_tokens: number, total_tokens: number}
interface IChoice {message: IMessage, finish_reason: string, index: number}
interface IChatCompletion {id: string, object: object, created: number, model: string, usage: IUsage, choices: IChoice[]}
