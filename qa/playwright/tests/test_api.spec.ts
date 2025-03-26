import { test, expect, APIRequestContext } from '@playwright/test';
import * as fs from 'fs';
import { load } from "js-yaml";

let apiContext: APIRequestContext;
const baseURL = process.env.API_BASE_URL;
const key = process.env.API_KEY;
const INPUT_FILEPATH_JSON = './data/test_data_records.json';
const INPUT_FILEPATH_YAML = './data/test_data_records.yaml';
const EXPORT_PATH_TO_DIR = './data/test_data';

type InputItemType = {
    _id: string;
    some_key: string;
};

let inputItems: Array<InputItemType>;

if (fs.existsSync(INPUT_FILEPATH_JSON)) {
    inputItems = JSON.parse(fs.readFileSync(INPUT_FILEPATH_JSON, 'utf8')) as Array<InputItemType>;
} else if (fs.existsSync(INPUT_FILEPATH_YAML)) {
    inputItems = load(fs.readFileSync(INPUT_FILEPATH_YAML, 'utf8')) as Array<InputItemType>;
} else {
    throw new Error('No input file found. Please provide a valid JSON or YAML file.');
}

function makeFolderIfNotExists(path: string) {
    if (!fs.existsSync(path)) {
        fs.mkdirSync(path, { recursive: true });
    }
};

test('environment variables', async () => {
    console.log(`baseURL: ${baseURL}`);
    console.log(`key: ${key}`);
    expect(baseURL).toBeDefined();
    expect(key).toBeDefined
});

test.describe('Test API', () => {
    // Request context is reused by all tests in the file.
    test.beforeAll(async ({ playwright }) => {
    apiContext = await playwright.request.newContext({
        // All requests we send go to this API endpoint.
        baseURL: `${baseURL}`,
        extraHTTPHeaders: {
        // We set this header per GitHub guidelines.
        'Accept': 'application/vnd.github.v3+json',
        // Add authorization token to all requests.
        // Assuming personal access token available in the environment.
        'Authorization': `${key}`,
        },
    });
    });

    test.afterAll(async ({ }) => {
        // Dispose all responses.
        await apiContext.dispose();
    });

    test('GET /api_route', async ({ request }) => {
        const startTime = Date.now();
        const response = await apiContext.get(`${baseURL}/api_route?param=foo`);
        const endTime = Date.now();
        const responseTime = endTime - startTime;
        console.log(`Response time: ${responseTime} ms`);
        console.log(response.status());
        expect(response.status()).toBe(200);
        const data = await response.json();
        console.log(data);
        expect(data).toHaveProperty('some_property');
    });

    test('GET /api_route expected to fail', async ({ request }) => {
        const response = await apiContext.get(`${baseURL}/api_route`);
        console.log(response.status());
        expect([400, 404]).toContain(response.status());
    });

    test('POST /api_route', async ({ request }) => {
        const startTime = Date.now();
        const response = await apiContext.post(`${baseURL}/api_route`, {
            data: {
                some_key: 'some_value',
            }
        });
        const endTime = Date.now();
        const responseTime = endTime - startTime;
        console.log(`Response time: ${responseTime} ms`);
        console.log(response.status());
        expect(response.status()).toBe(200);
        const data = await response.json();
        console.log(data);
        expect(data).toHaveProperty('array_in_result');
        const array_in_result = data.array_in_result;
        expect(Array.isArray(array_in_result)).toBe(true);
        array_in_result.forEach((item: any) => {
            expect(item).toHaveProperty('some_property');
        });
    });

    test('POST /api_route expected to fail', async ({ request }) => {
        const response = await apiContext.post(`${baseURL}/api_route`);
        console.log(response.status());
        expect(response.status()).toBe(400);
    });

    inputItems.forEach((inputItem) => {
        test(`GET /api_route for inputItem ${inputItem._id}`, async ({ request }) => {
            const startTime = Date.now();
            const response = await apiContext.get(`${baseURL}/api_route?param=foo`);
            const endTime = Date.now();
            const responseTime = endTime - startTime;
            console.log(`Response time for ${inputItem._id}: ${responseTime} ms`);
            console.log(response.status());
            expect(response.status()).toBe(200);
            const data = await response.json();
            console.log(data);
            expect(data).toHaveProperty('some_property');
            const some_property = data.some_property;

            // Build metadata and export as JSON file
            const metadata = {
                _id: inputItem._id,
                createdAt: new Date().toISOString(),
                responseTime: responseTime,
                env: { baseURL }
            };
            const exportData = {
                some_property,
                metadata
            };
            try {
                makeFolderIfNotExists(EXPORT_PATH_TO_DIR);
                const filename = `${EXPORT_PATH_TO_DIR}/export.json`;
                fs.writeFileSync(filename, JSON.stringify(exportData, null, 2), 'utf-8');
            } catch (error) {
                console.error(`Error exporting data for ${inputItem._id}: ${error}`);
            }
        });
    };
});