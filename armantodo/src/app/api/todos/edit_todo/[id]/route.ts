import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';


export async function PUT(req: NextRequest, { params }: { params: { id: string } }) {
    const id = params.id
    if (!Number.isInteger(Number(id))) {
        return NextResponse.json({ error: 'Invalid ID' }, { status: 400 });
    }
    try {
        const formData = await req.formData();
        const title = formData.get('title')?.toString() || '';
        const description = formData.get('description')?.toString() || '';

        const todo = await prisma.todo.update({
            where: { id: Number(id) },
            data: { title, description },
        });
        return NextResponse.json(todo, { status: 200 });
    } catch (error: any) {
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}