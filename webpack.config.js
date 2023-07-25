//@ts-check

'use strict';

const path = require('path');

//@ts-check
/** @typedef {import('webpack').Configuration} WebpackConfig **/

/** @type WebpackConfig */
const extensionConfig = {
    target: 'node', // vscode extensions run in a Node.js-context 📖 -> https://webpack.js.org/configuration/node/
    mode: 'none', // this leaves the source code as close as possible to the original (when packaging we set this to 'production')

    entry: './src/extension.ts', // the entry point of this extension, 📖 -> https://webpack.js.org/configuration/entry-context/
    output: {
        // the bundle is stored in the 'dist' folder (check package.json), 📖 -> https://webpack.js.org/configuration/output/
        path: path.resolve(__dirname, 'dist'),
        filename: 'extension.js',
        libraryTarget: 'commonjs2',
    },
    externals: [
        { vscode: 'commonjs vscode' }, // the vscode-module is created on-the-fly and must be excluded. Add other modules that cannot be webpack'ed, 📖 -> https://webpack.js.org/configuration/externals/
        '@azure/functions-core',
        'applicationinsights-native-metrics',
        // modules added here also need to be added in the .vscodeignore file
    ],
    ignoreWarnings: [
        {
            module: /@opentelemetry\/instrumentation\/build\/esm\/platform\/node\/instrumentation\.js/,
            message: /the request of a dependency is an expression/,
        },
    ],
    resolve: {
        // support reading TypeScript and JavaScript files, 📖 -> https://github.com/TypeStrong/ts-loader
        extensions: ['.ts', '.js'],
    },
    module: {
        rules: [
            {
                test: /\.ts$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: 'ts-loader',
                    },
                ],
            },
        ],
    },
    devtool: 'source-map',
    infrastructureLogging: {
        level: 'log', // enables logging required for problem matchers
    },
};
module.exports = [extensionConfig];
