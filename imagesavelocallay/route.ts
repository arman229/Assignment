

import fs from 'fs';
import path from 'path';
import { put } from '@vercel/blob';
import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';
export function getFileOrThrow(formData: FormData, key: string): File {
    const formDataValue = formData.get(key);
    if (!formDataValue) {
        throw new Error(`File for key "${key}" not found`);
    }
    if (!(formDataValue instanceof File)) {
        throw new Error(`Value for key "${key}" is not a valid File`);
    }
    return formDataValue;


    async function saveFileToLocal(logoFile: File) {
        const uploadDir = path.join(process.cwd(), 'public', 'uploads');
        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir, { recursive: true });
        }
        const filePath = path.join(uploadDir, logoFile.name);
        const fileBuffer = await streamToBuffer(logoFile.stream());
        await fs.promises.writeFile(filePath, fileBuffer);
    }

    async function streamToBuffer(stream: ReadableStream<Uint8Array>): Promise<Buffer> {
        const chunks: Uint8Array[] = [];
        const reader = stream.getReader();
        let done, value;

        while ({ done, value } = await reader.read()) {
            if (done) break;
            if (value)
                chunks.push(value);
        }

        return Buffer.concat(chunks);
    }
    export async function POST(req: NextRequest) {
        try {
            const formData = await req.formData();
            const logoFile = getFileOrThrow(formData, 'logo');
            await saveFileToLocal(logoFile)
            const company = await prisma.company.create({
                data: { logoFile },
            });

            return NextResponse.json({ "message": "image save successfully" }, { status: 201 });
        } catch (error: any) {
            return NextResponse.json({ message: error.message }, { status: 500 });
        }
    }
