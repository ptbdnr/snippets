import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';

// Basic tests

describe('Basic tests', () => {
    it('should pass basic test', () => {
        expect(1).toBe(1);
    });
});

// Failing tests

describe('Failing tests', () => {
    it('should throw an error', () => {
        const functionExpectedToThrow = () => {
            throw new Error('Expected error');
        };
        expect(() => functionExpectedToThrow()).toThrowError('Expected error');
    });
});

// Parametrization

describe('Parametrization', () => {
    const cases = [
        [1, 2],
        [2, 3],
    ];

    it.each(cases)('should add 1 to %i to get %i', (input, expected) => {
        expect(input + 1).toBe(expected);
    });
});

// Exceptions

describe('Exceptions', () => {
    it('should raise exception', () => {
        expect(() => {
            throw new Error('ZeroDivisionError');
        }).toThrow('ZeroDivisionError');
    });
});

// Skips

describe('Skips', () => {
    it.skip('should skip this test', () => {
        expect(1).toBe(2);
    });

    const SKIP_IF_TRUE = true;

    if (SKIP_IF_TRUE) {
        it.skip('should skip if true', () => {
            expect(1).toBe(2);
        });
    }
});

// Fixtures

describe('Fixtures', () => {
    let sampleFixture: number;

    beforeEach(() => {
        sampleFixture = 42;
    });

    it('should use fixture', () => {
        expect(sampleFixture).toBe(42);
    });

    let sampleFixtureWithTeardown: number;

    beforeEach(() => {
        sampleFixtureWithTeardown = 42;
    });

    afterEach(() => {
        console.log('teardown');
    });

    it('should use fixture with teardown', () => {
        expect(sampleFixtureWithTeardown).toBe(42);
    });
});
