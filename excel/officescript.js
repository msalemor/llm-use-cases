async function main(workbook: ExcelScript.Workbook) {
    const sheet = workbook.getWorksheet("Sheet1");
    const messages : IMessage[] =  [{
        role: "user", content: sheet.getRange("c2").getValue().toString()
    }];
    const payload: IPrompt = {
        messages, // TODO: Get from cells
        max_tokens: 100, // TODO: Get from cell
        temperature: 0.3 // TODO: Get from cell
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
    const gptURI = 'https://<NAME>.openai.azure.com/openai/deployments/<DEPLOYMENT_NAME>/chat/completions?api-version=2023-07-01-preview';
    const response = await fetch(gptURI, settings);
    const completion: IChatCompletion = await response.json();    
    sheet.getRange("c4").setValue(completion.choices[0].message.content); //TODO: Maybe parse output across cells
}
// GPT Interfaces
interface IPrompt { messages: IMessage[], max_tokens: number, temperature: number }
interface IMessage {role: string, content: string}
interface IUsage {prompt_tokens: number, completion_tokens: number, total_tokens: number}
interface IChoice {message: IMessage, finish_reason: string, index: number}
interface IChatCompletion {id: string, object: object, created: number, model: string, usage: IUsage, choices: IChoice[]}
