import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';
export async function GET(req: NextRequest) {
    try {
        const todo = await prisma.todo.findMany({
            orderBy: {
                id: 'asc',
            },
        });
        return NextResponse.json(todo);
    } catch (error: any) {
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
