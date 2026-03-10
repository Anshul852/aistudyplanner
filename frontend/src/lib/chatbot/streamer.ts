export class Streamer {

    async stream(
        messageId: string,
        text: string,
        updateFn: (id: string, updates: any) => void
    ): Promise<void> {

        let displayed = ''

        for (let i = 0; i < text.length; i++) {
            const char = text[i]
            displayed += char

            updateFn(messageId, {
                content: displayed,
                isStreaming: true
            })

            // varied delay for natural feel
            const delay = this.getDelay(char, text[i + 1])
            await this.sleep(delay)
        }

        // finalize
        updateFn(messageId, {
            content: text,
            isStreaming: false
        })
    }

    private getDelay(char: string, nextChar?: string): number {
        if (char === '.') return 200 + Math.random() * 200
        if (char === ',') return 80 + Math.random() * 70
        if (char === '!') return 150 + Math.random() * 100
        if (char === '?') return 150 + Math.random() * 100
        if (char === '\n') return 100
        // random thinking pause 5% of the time
        if (Math.random() < 0.05) return 300 + Math.random() * 300
        return 15 + Math.random() * 25
    }

    private sleep(ms: number): Promise<void> {
        return new Promise(resolve => setTimeout(resolve, ms))
    }
}
