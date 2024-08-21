
import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';
export async function POST(req: NextRequest) {
    try {
        const formData = await req.formData();
        const title = formData.get('title')?.toString() || '';
        const description = formData.get('description')?.toString() || '';
    
        const todo = await prisma.todo.create({
            data: {
                title,
                description,
        
            },
        });
        return NextResponse.json(todo, { status: 201 });
    } catch (error: any) {
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
